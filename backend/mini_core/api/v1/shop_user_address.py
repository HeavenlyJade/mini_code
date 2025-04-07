from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required

from backend.business.service.auth import auth_required
from backend.mini_core.domain.t_user import ShopUserAddress
from backend.mini_core.schema.shop_user import (
    ShopUserAddressCreateSchema,
    ShopUserAddressListSchema,
    ShopUserAddressQueryArgSchema,
    ShopUserAddressSchema,
    ShopUserAddressUpdateSchema,
    SetDefaultAddressSchema
)
from backend.mini_core.service import shop_user_address_service
from kit.schema.base import RespSchema
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('shop_user_addresses', 'shop_user_addresses', url_prefix='/shop_user_addresses')


@blp.route('/all')
class AllShopUserAddressesAPI(MethodView):
    """查看所有商城用户地址API（管理员后台使用）"""

    decorators = [auth_required()]

    @blp.arguments(ShopUserAddressQueryArgSchema, location='query')
    @blp.response(ShopUserAddressListSchema)
    def get(self, args: dict):
        """管理员查看所有用户地址列表

        管理员可查看系统中所有用户的地址信息，支持分页和筛选
        """
        # 直接调用list方法，不做用户ID过滤
        return shop_user_address_service.list(args)

@blp.route('/')
class ShopUserAddressAPI(MethodView):
    """商城用户地址API"""

    decorators = [jwt_required()]

    @blp.arguments(ShopUserAddressQueryArgSchema, location='query')
    @blp.response(ShopUserAddressListSchema)
    def get(self, args: dict):
        """商城用户地址 查看地址列表"""
        user_id = get_jwt_identity()
        return shop_user_address_service.get_user_addresses(user_id)

    @blp.arguments(ShopUserAddressCreateSchema)
    @blp.response(ShopUserAddressSchema)
    def post(self, address: ShopUserAddress):
        """商城用户地址 创建地址"""
        user_id = get_jwt_identity()
        address.user_id = user_id
        return shop_user_address_service.create(address)


@blp.route('/<int:address_id>')
class ShopUserAddressByIDAPI(MethodView):
    decorators = [jwt_required()]

    @blp.response(ShopUserAddressSchema)
    def get(self, address_id: int):
        """商城用户地址 查看地址详情"""
        return shop_user_address_service.get(address_id)

    @blp.arguments(ShopUserAddressUpdateSchema)
    @blp.response(ShopUserAddressSchema)
    def put(self, address: ShopUserAddress, address_id: int):
        """商城用户地址 编辑地址"""
        return shop_user_address_service.update(address_id, address)

    @blp.response(RespSchema)
    def delete(self, address_id: int):
        """商城用户地址 删除地址"""
        shop_user_address_service.delete(address_id)
        return {'code': 200, 'msg': '删除成功'}


@blp.route('/default')
class DefaultAddressAPI(MethodView):
    decorators = [jwt_required()]

    @blp.response(ShopUserAddressSchema)
    def get(self):
        """商城用户地址 获取默认地址"""
        user_id = get_jwt_identity()
        return shop_user_address_service.get_default_address(user_id)

    @blp.arguments(SetDefaultAddressSchema)
    @blp.response(RespSchema)
    def post(self, args: dict):
        """商城用户地址 设置默认地址"""
        user_id = get_jwt_identity()
        return shop_user_address_service.set_default(args['address_id'], user_id)


@blp.route('/user/<user_id>')
class ShopUserAddressByUserAPI(MethodView):
    """管理员查看商城用户地址API"""

    decorators = [auth_required()]

    @blp.response(ShopUserAddressListSchema)
    def get(self, user_id: str):
        """管理员查看商城用户地址列表"""
        return shop_user_address_service.get_user_addresses(user_id)
