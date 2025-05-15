from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_current_user

from backend.business.service.auth import auth_required
from backend.mini_core.schema.order.shop_order_review import (
    OrderReviewQueryArgSchema, OrderReviewCreateSchema, OrderReviewReplySchema,
    OrderReviewStatusUpdateSchema, OrderReviewTopUpdateSchema,
    OrderReviewResponseSchema, OrderReviewListResponseSchema, OrderReviewStatsResponseSchema
)
from backend.mini_core.service import order_review_service
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('order_review', 'order_review', url_prefix='/order-reviews')


@blp.route('/')
class OrderReviewAPI(MethodView):
    """订单评价API"""

    @blp.arguments(OrderReviewQueryArgSchema, location='query')
    @blp.response(OrderReviewListResponseSchema)
    def get(self, args):
        """查询评价列表"""
        return order_review_service.get_product_reviews(args)

    @jwt_required()
    @blp.arguments(OrderReviewCreateSchema)
    @blp.response(OrderReviewResponseSchema)
    def post(self, review_data):
        """创建商品评价"""
        return order_review_service.create_review(review_data)


@blp.route('/<int:review_id>')
class OrderReviewDetailAPI(MethodView):
    """订单评价详情API"""

    @blp.response(OrderReviewResponseSchema)
    def get(self, review_id):
        """获取评价详情"""
        review = order_review_service.get(review_id)
        return dict(data=review, code=200)

    @jwt_required()
    @blp.response(OrderReviewResponseSchema)
    def delete(self, review_id):
        """删除评价"""
        # 获取当前用户
        current_user = get_current_user()

        # 获取评价
        review = order_review_service.get(review_id)
        if not review:
            return dict(code=404, message="评价不存在")

        # 检查权限
        if str(review.user_id) != str(current_user.id):
            return dict(code=403, message="无权删除该评价")

        # 删除评价
        order_review_service.delete(review_id)
        return dict(code=200, message="评价已删除")


@blp.route('/product/<int:product_id>')
class ProductReviewsAPI(MethodView):
    """商品评价API"""

    @blp.arguments(OrderReviewQueryArgSchema, location='query')
    @blp.response(OrderReviewListResponseSchema)
    def get(self, args, product_id):
        """获取商品评价列表"""
        args['product_id'] = product_id
        return order_review_service.get_product_reviews(args)


@blp.route('/user')
class UserReviewsAPI(MethodView):
    """用户评价API"""

    @jwt_required()
    @blp.response(OrderReviewListResponseSchema)
    def get(self):
        """获取当前用户的评价列表"""
        current_user = get_current_user()
        return order_review_service.get_user_reviews(current_user.id)


@blp.route('/order/<string:order_no>')
class OrderReviewsAPI(MethodView):
    """订单评价列表API"""

    @blp.response(OrderReviewListResponseSchema)
    def get(self, order_no):
        """获取订单的评价列表"""
        return order_review_service.get_order_reviews(order_no)


@blp.route('/reply')
class ReviewReplyAPI(MethodView):
    """评价回复API"""

    @auth_required()
    @blp.arguments(OrderReviewReplySchema)
    @blp.response(OrderReviewResponseSchema)
    def post(self, reply_data):
        """商家回复评价"""
        return order_review_service.reply_review(reply_data['review_id'], reply_data['reply_content'])


@blp.route('/status')
class ReviewStatusAPI(MethodView):
    """评价状态API"""

    @auth_required()
    @blp.arguments(OrderReviewStatusUpdateSchema)
    @blp.response(OrderReviewResponseSchema)
    def post(self, status_data):
        """更新评价状态"""
        return order_review_service.update_review_status(status_data['review_id'], status_data['status'])


@blp.route('/top')
class ReviewTopAPI(MethodView):
    """评价置顶API"""

    @auth_required()
    @blp.arguments(OrderReviewTopUpdateSchema)
    @blp.response(OrderReviewResponseSchema)
    def post(self, top_data):
        """设置评价置顶状态"""
        return order_review_service.set_top_status(top_data['review_id'], top_data['is_top'])


@blp.route('/statistics/product/<int:product_id>')
class ReviewStatisticsAPI(MethodView):
    """评价统计API"""

    @blp.response(OrderReviewStatsResponseSchema)
    def get(self, product_id):
        """获取商品评价统计数据"""
        return order_review_service.get_review_statistics(product_id)
