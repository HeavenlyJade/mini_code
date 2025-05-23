import datetime as dt
import random
import time
from typing import Optional, Dict, Any, Union, Type

from flask import g
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_jwt_identity,
)
from werkzeug.security import check_password_hash, generate_password_hash

from backend.mini_core.domain.t_user import ShopUser, ShopUserAddress
from backend.mini_core.message.shop_user import ShopUserMessage
from backend.mini_core.repository.shop.shop_user_sqla import ShopUserSQLARepository, ShopUserAddressSQLARepository
from kit.domain.entity import Entity, EntityInt
from kit.exceptions import ServiceBadRequest
from kit.service.base import CRUDService

__all__ = ['ShopUserService', 'ShopUserAddressService']


def _generate_user_id() -> str:
    """生成商城用户编号"""
    # 基于时间戳生成唯一编号 (格式: U + 时间戳 + 3位随机数)
    timestamp = int(time.time())
    random_num = random.randint(100, 999)
    return f"U{timestamp}{random_num}"


class ShopUserService(CRUDService[ShopUser]):
    def __init__(self, repo: ShopUserSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> ShopUserSQLARepository:
        return self._repo

    def get(self, user_id: int) -> Type[Union[Entity, EntityInt, ShopUser]]:
        """获取商城用户详情"""
        user = get_current_user()
        user_id_cache = user.id
        if user_id_cache != user_id:
            raise ServiceBadRequest("错误的请求用户")
        return self._repo.find(id=user_id)

    def find(self, **kwargs):
        return self._repo.find(**kwargs)

    def create(self, user: ShopUser) -> Entity:
        """创建商城用户"""
        # 生成用户编号
        user.user_id = _generate_user_id()

        # 如果提供了密码，对其进行哈希处理
        if user.password:
            user.password = generate_password_hash(user.password)

        # 记录注册时间
        user.register_time = dt.datetime.now()

        # 获取当前用户信息（如果有）
        try:
            current_user = get_current_user()
            if current_user:
                user.creator = current_user.username
        except:
            user.creator = "admin"
        return   self._repo.create(user)

    def admin_update(self,entity_id, user: ShopUser):
        # 记录更新者
        current_user = get_current_user()
        if current_user:
            user.updater = current_user.username
        re_data = self._repo.update(entity_id, user)
        return dict(data=re_data,code=200)

    def update(self, entity_id: int, user: ShopUser) -> Optional[ShopUser]:
        """更新商城用户信息"""
        # 如果提供了密码，对其进行哈希处理
        user_cache = get_current_user()
        user_id_cache = user_cache.id
        if user_id_cache != entity_id:
            raise ServiceBadRequest("错误的请求用户")
        if user.password:
            user.password = generate_password_hash(user.password)

        # 记录更新者
        current_user = get_current_user()
        if current_user:
            user.updater = current_user.username
        return self._repo.update(entity_id, user)

    def delete(self, entity_id: int) -> None:
        """删除商城用户"""
        # 检查用户是否存在
        user = self.get(entity_id)
        if not user:
            raise ServiceBadRequest(ShopUserMessage.USER_NOT_EXIST)

        # 调用父类方法执行删除
        return super().delete(entity_id)

    def update_status(self, user_id: int, status: int) -> ShopUser:
        """更新商城用户状态"""
        user = self.repo.update_user_status(user_id, status)
        if not user:
            raise ServiceBadRequest(ShopUserMessage.USER_NOT_EXIST)
        return user

    def login(self, args: dict) -> Dict[str, Any]:
        """商城用户登录"""
        username_or_phone = args['username']
        password = args['password']

        # 尝试通过用户名查找用户
        user = self.repo.get_by_username(username_or_phone)

        # 如果未找到，再尝试通过手机号查找用户
        if not user:
            user = self.repo.get_by_phone(username_or_phone)

        # 用户不存在或已停用
        if not user or user.status == 0:
            raise ServiceBadRequest(ShopUserMessage.USER_NOT_EXIST)

        # 验证密码
        if not self._verify_password(user.password, password):
            raise ServiceBadRequest(ShopUserMessage.USER_PASSWORD_ERROR)

        # 更新登录信息
        user.last_login_time = dt.datetime.now()
        if hasattr(g, 'ip'):
            user.last_login_ip = g.ip
        self.repo.update(user.id, user)

        # 生成令牌
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user_info': user,
            'code': 200,
            'msg': '登录成功'
        }

    def wechat_login(self, args: dict) -> Dict[str, Any]:
        """微信登录"""
        code = args['code']
        user_info = args.get('user_info', {})

        # TODO: 调用微信API获取openid和用户信息
        # 这里简化处理，假设已经获取到了openid
        openid = f"wx_{code}"  # 实际开发中应该调用微信API获取真实的openid

        # 查找是否已存在该openid对应的用户
        user = self.repo.get_by_openid(openid)

        # 如果用户不存在，则创建新用户
        if not user:
            user = ShopUser(
                openid=openid,
                nickname=user_info.get('nickName', '微信用户'),
                avatar=user_info.get('avatar', ''),
                gender=user_info.get('gender', 0),
                status=1,
                register_channel='微信小程序',
                register_time=dt.datetime.now()
            )
            user = self.create(user)

        # 更新登录信息
        user.last_login_time = dt.datetime.now()
        if hasattr(g, 'ip'):
            user.last_login_ip = g.ip
        self.repo.update(user.id, user)

        # 生成令牌
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user_info': user,
            'code': 200,
            'msg': '登录成功'
        }

    def refresh_token(self):
        """刷新token"""
        openid = get_jwt_identity()
        return {
            'access_token': create_access_token(identity=openid),
            'code': 200
        }

    def get_or_create_wechat_user(self, user_data: Dict[str, Any]) -> ShopUser:
        """
        查找或创建微信用户

        Args:
            user_data: 包含以下字段的字典:
                - openid: 微信用户的openid
                - username: 用户名
                - nickName: 微信昵称
                - avatar: 头像URL
                - appid: 微信应用ID

        Returns:
            ShopUser: 返回找到或新创建的用户对象
        """
        from backend.mini_core.service import  distribution_service
        # 首先尝试通过openid查找用户
        openid = user_data.get('openid')
        if not openid:
            raise ServiceBadRequest("微信用户标识(openid)不能为空")

        user = self.repo.get_by_openid(openid)

        # 如果用户存在，更新必要的字段
        if user:
            user.last_login_time = dt.datetime.now()
            self.repo.update(user.id, user)
        else:
            new_user = ShopUser(
                openid=openid,
                user_id=_generate_user_id(),  # 生成用户ID
                username=user_data.get('username', f"wx_user_{openid[-8:]}"),  # 生成默认用户名
                nickname=user_data.get('nickName', '微信用户'),
                unionid=user_data.get('appid', ''),
                avatar=user_data.get('avatar', ''),
                status=1,  # 默认启用状态
                register_channel='微信小程序',
                register_time=dt.datetime.now(),
                mini_program_name=user_data.get('appid', '')  # 存储appid到mini_program_name字段
            )
            user = self.create(new_user)
        dis_user_data = distribution_service.get({"sn": openid}).get("data")
        if not dis_user_data:
            share_user_id = user_data.get('share_user_id')
            create_data = dict(sn=openid, total_amount=0, lv_id=2, user_id=user.user_id)
            if share_user_id != user.user_id:
                create_data['user_father_id'] = share_user_id
            distribution_service.create(create_data)
        return user

    @classmethod
    def _verify_password(cls, pw_hash: str, password: str) -> bool:
        """验证密码"""
        return check_password_hash(pw_hash, password)


class ShopUserAddressService(CRUDService[ShopUserAddress]):
    def __init__(self, repo: ShopUserAddressSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> ShopUserAddressSQLARepository:
        return self._repo

    def get_user_addresses(self, user_id: str) -> Dict[str, Any]:
        """获取用户地址列表"""
        addresses = self.repo.get_user_addresses(user_id)
        return {
            'items': addresses,
            'total': len(addresses),
            'code': 200
        }

    def get_default_address(self, user_id: str) -> Optional[ShopUserAddress]:
        """获取用户默认地址"""
        return self.repo.get_default_address(user_id)

    def create(self, address: ShopUserAddress) -> dict[str, Union[int, Entity]]:
        """创建用户地址"""
        # 如果是默认地址，则将其他地址设为非默认
        if address.is_default == 1:
            self.repo.set_default_address(0, address.user_id)  # 0表示没有一个是默认地址
        # 记录创建者
        current_user = get_current_user()
        if current_user:
            address.creator = current_user.username
        re_data = self.repo.create(address)
        return dict(code=200, data=re_data)

    def find_address(self, address_id: int, user_id: str):
        address = self.get(address_id)
        if not address or address.user_id != user_id:
            raise ServiceBadRequest("地址不存在或不属于该用户")
        return dict(code=200, data=address)

    def get_address(self, user_id: str) -> dict[str, list[Entity]]:
        from kit.util.sqla import validate_user_entity_match
        validate_user_entity_match(user_id)
        re_data = self.repo.find_all(user_id=str(user_id))
        return dict(items=re_data, code=200)

    def set_default_address(self, address_id: int, ):
        user_cache = get_current_user()
        user_id_cache = user_cache.id
        original_address = self.get(address_id)
        if not original_address:
            raise ServiceBadRequest("地址不存在")
        if str(original_address.user_id) != str(user_id_cache):
            raise ServiceBadRequest("错误的用户，1006")
        self.repo.set_default_address(address_id, str(user_id_cache))
        return dict(code=200)

    def update(self, entity_id: int, address: ShopUserAddress) -> dict[str, Union[int, Entity, None]]:
        """更新用户地址"""
        # 获取原地址信息
        original_address = self.get(entity_id)
        if not original_address:
            raise ServiceBadRequest("地址不存在")

        # 如果设置为默认地址，则将用户其他地址设为非默认
        if address.is_default == 1 and original_address.is_default != 1:
            self.repo.set_default_address(entity_id, original_address.user_id)
        # 记录更新者
        current_user = get_current_user()
        if current_user:
            address.updater = current_user.username
        re_data = self.repo.update(entity_id, address)
        return dict(code=200, data=re_data)

    def set_default(self, address_id: int, user_id: str) -> Dict[str, Any]:
        """设置默认地址"""
        # 检查地址是否存在且属于该用户
        address = self.get(address_id)
        if not address or address.user_id != user_id:
            raise ServiceBadRequest("地址不存在或不属于该用户")

        # 设置为默认地址
        self.repo.set_default_address(address_id, user_id)

        return {
            'code': 200,
            'msg': '设置默认地址成功'
        }

    def delete_user_addr(self, address_id: int, user_id: str) -> None:
        address = self.get(address_id)
        if not address or address.user_id != user_id:
            raise ServiceBadRequest("地址不存在或不属于该用户")
        self.repo.delete(address_id)
