import datetime as dt
from typing import List, Optional, Tuple, Type
from sqlalchemy import BigInteger, Column, DateTime, String, Table, Text, Integer, Date, DECIMAL, Boolean, and_, or_, \
    desc
from sqlalchemy import event

from backend.extensions import mapper_registry
from backend.mini_core.domain.t_user import ShopUser, ShopUserAddress
from backend.mini_core.message.shop_user import ShopUserMessage
from kit.exceptions import ServiceBadRequest
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column

__all__ = ['ShopUserSQLARepository', 'ShopUserAddressSQLARepository']

# 商城用户表
shop_user_table = Table(
    't_shop_user',
    mapper_registry.metadata,
    id_column(),
    Column('user_id', String(32), unique=True, comment='用户编号'),
    Column('username', String(64), unique=True, comment='用户名'),
    Column('nickname', String(64), comment='昵称'),
    Column('phone', String(20), comment='手机号码'),
    Column('email', String(128), comment='邮箱地址'),
    Column('password', String(128), comment='登录密码(加密存储)'),
    Column('avatar', String(255), comment='头像URL'),
    Column('openid', String(64), comment='微信openid'),
    Column('unionid', String(64), comment='微信unionid'),
    Column('mini_program_name', String(64), comment='小程序名称'),
    Column('register_channel', String(32), comment='注册渠道'),
    Column('register_shop_id', BigInteger, comment='所属门店ID'),
    Column('register_shop_name', String(64), comment='所属门店名称'),
    Column('real_name', String(64), comment='真实姓名'),
    Column('gender', Integer, comment='性别(0-未知,1-男,2-女)'),
    Column('birthday', Date, comment='生日'),
    Column('address', Text, comment='详细地址'),
    Column('member_level', String(32), comment='会员等级'),
    Column('member_card_no', String(64), comment='会员卡号'),
    Column('points', Integer, comment='积分'),
    Column('balance', DECIMAL(10, 2), comment='账户余额'),
    Column('is_distributor', Integer, default=0, comment='是否分销商(1-是,0-否)'),
    Column('tags', String(255), comment='标签(多个用逗号分隔)'),
    Column('remark', Text, comment='备注'),
    Column('status', Integer, default=1, comment='状态(1-正常,0-停用)'),
    Column('last_login_time', DateTime, comment='最后登录时间'),
    Column('last_login_ip', String(64), comment='最后登录IP'),
    Column('register_time', DateTime, comment='成为会员时间'),
    Column('register_ip', String(64), comment='注册IP'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
    Column('updater', String(64), comment='更新人'),
    Column('avatarurl', String(255), comment='头像路径'),

)

# 商城用户地址表
shop_user_address_table = Table(
    't_shop_user_address',
    mapper_registry.metadata,
    id_column(),
    Column('user_id', String(32), nullable=False, comment='用户编号'),
    Column('receiver_name', String(64), nullable=False, comment='收货人姓名'),
    Column('receiver_phone', String(20), nullable=False, comment='收货人电话'),
    Column('province', String(32), comment='省份'),
    Column('city', String(32), comment='城市'),
    Column('district', String(32), comment='区/县'),
    Column('detail_address', String(255), nullable=False, comment='详细地址'),
    Column('postal_code', String(20), comment='邮政编码'),
    Column('is_default', Integer, default=0, comment='是否默认地址(1-是,0-否)'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
    Column('updater', String(64), comment='更新人'),
)

# 映射
mapper_registry.map_imperatively(ShopUser, shop_user_table)
mapper_registry.map_imperatively(ShopUserAddress, shop_user_address_table)


class ShopUserSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[ShopUser]:
        return ShopUser

    @property
    def query_params(self) -> Tuple:
        return ('user_id', 'status', 'gender', 'register_shop_id', 'is_distributor')

    @property
    def fuzzy_query_params(self) -> Tuple:
        return ('username', 'nickname', 'phone', 'email', 'real_name', 'tags')

    @property
    def range_query_params(self) -> Tuple:
        return ('register_time', 'last_login_time', 'points', 'balance')

    def get_by_username(self, username: str) -> Optional[ShopUser]:
        """通过用户名获取用户"""
        return self.session.query(ShopUser).filter(ShopUser.username == username).first()

    def get_by_phone(self, phone: str) -> Optional[ShopUser]:
        """通过手机号获取用户"""
        return self.session.query(ShopUser).filter(ShopUser.phone == phone).first()

    def get_by_openid(self, openid: str) -> Optional[ShopUser]:
        """通过微信openid获取用户"""
        return self.session.query(ShopUser).filter(ShopUser.openid == openid).first()

    def update_user_status(self, user_id: int, status: int) -> Optional[ShopUser]:
        """更新用户状态"""
        user = self.get_by_id(user_id)
        if user:
            user.status = status
            self.session.commit()
        return user


class ShopUserAddressSQLARepository( SQLARepository):
    @property
    def model(self) -> Type[ShopUserAddress]:
        return ShopUserAddress

    @property
    def query_params(self) -> Tuple:
        return ('user_id', 'is_default')

    @property
    def fuzzy_query_params(self) -> Tuple:
        return ('receiver_name', 'receiver_phone', 'detail_address')

    def get_user_addresses(self, user_id: str) -> List[ShopUserAddress]:
        """获取用户的所有地址"""
        return self.session.query(ShopUserAddress).filter(ShopUserAddress.user_id == user_id).all()

    def get_default_address(self, user_id: str) -> Optional[ShopUserAddress]:
        """获取用户的默认地址"""
        return self.session.query(ShopUserAddress).filter(
            and_(ShopUserAddress.user_id == user_id, ShopUserAddress.is_default == 1)
        ).first()

    def set_default_address(self, address_id: int, user_id: str) -> None:
        """设置用户的默认地址"""
        # 先将用户所有地址设为非默认
        self.session.query(ShopUserAddress).filter(
            ShopUserAddress.user_id == user_id
        ).update({'is_default': 0})

        # 设置指定地址为默认
        self.session.query(ShopUserAddress).filter(
            ShopUserAddress.id == address_id
        ).update({'is_default': 1})

        self.session.commit()


# ShopUser表的事件监听器
@event.listens_for(ShopUser, 'before_insert')
def shop_user_before_insert(mapper, connection, target: ShopUser):
    # 检查用户名唯一性
    from backend.extensions import db
    if target.username and db.session.query(ShopUser).filter(ShopUser.username == target.username).first():
        raise ServiceBadRequest(ShopUserMessage.USER_EXISTED)

    # 检查手机号唯一性
    if target.phone and db.session.query(ShopUser).filter(ShopUser.phone == target.phone).first():
        raise ServiceBadRequest(ShopUserMessage.PHONE_EXISTED)

    # 检查openid唯一性
    if target.openid and db.session.query(ShopUser).filter(ShopUser.openid == target.openid).first():
        raise ServiceBadRequest(ShopUserMessage.OPENID_EXISTED)


@event.listens_for(ShopUser, 'before_update')
def shop_user_before_update(mapper, connection, target: ShopUser):
    # 检查用户名唯一性
    from backend.extensions import db
    if target.username:
        existing = db.session.query(ShopUser).filter(
            and_(ShopUser.username == target.username, ShopUser.id != target.id)
        ).first()
        if existing:
            raise ServiceBadRequest(ShopUserMessage.USER_EXISTED)

    # 检查手机号唯一性
    if target.phone:
        existing = db.session.query(ShopUser).filter(
            and_(ShopUser.phone == target.phone, ShopUser.id != target.id)
        ).first()
        if existing:
            raise ServiceBadRequest(ShopUserMessage.PHONE_EXISTED)

    # 检查openid唯一性
    if target.openid:
        existing = db.session.query(ShopUser).filter(
            and_(ShopUser.openid == target.openid, ShopUser.id != target.id)
        ).first()
        if existing:
            raise ServiceBadRequest(ShopUserMessage.OPENID_EXISTED)
