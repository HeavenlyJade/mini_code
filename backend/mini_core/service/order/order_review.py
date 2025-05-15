import datetime as dt
import json
from typing import Dict, Any, List, Optional
from flask import g, current_app, request
from flask_jwt_extended import get_current_user

from kit.service.base import CRUDService
from backend.mini_core.domain.order.order_review import OrderReview
from backend.mini_core.repository.order.order_review import OrderReviewSQLARepository

__all__ = ['OrderReviewService']


class OrderReviewService(CRUDService[OrderReview]):
    def __init__(self, repo: OrderReviewSQLARepository):
        super().__init__(repo)
        self._repo = repo
        self._order_service = None  # 在使用时初始化，避免循环引用
        self._product_service = None  # 在使用时初始化，避免循环引用
        self._user_service = None  # 在使用时初始化，避免循环引用

    @property
    def repo(self) -> OrderReviewSQLARepository:
        return self._repo

    @property
    def order_service(self):
        """获取订单服务实例"""
        if self._order_service is None:
            # 延迟导入，避免循环引用
            from backend.mini_core.service import shop_order_service
            self._order_service = shop_order_service
        return self._order_service

    @property
    def product_service(self):
        """获取商品服务实例"""
        if self._product_service is None:
            # 延迟导入，避免循环引用
            from backend.mini_core.service import shop_product_service
            self._product_service = shop_product_service
        return self._product_service

    @property
    def user_service(self):
        """获取用户服务实例"""
        if self._user_service is None:
            # 延迟导入，避免循环引用
            from backend.mini_core.service import shop_user_service
            self._user_service = shop_user_service
        return self._user_service

    def get_product_reviews(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取商品评价列表

        参数:
            args: 查询参数，包含以下字段:
                - product_id: 商品ID
                - page: 页码
                - size: 每页大小
                - rating: 评分过滤
                - has_image: 是否只查询有图评价
                - ordering: 排序方式

        返回:
            包含评价列表和统计信息的字典
        """
        product_id = args.get('product_id')
        if not product_id:
            return dict(code=400, message="商品ID不能为空")

        # 构建查询参数
        query_params = {
            'product_id': product_id,
            'status': '已发布',
            'page': args.get('page', 1),
            'size': args.get('size', 10),
            'need_total_count': True
        }

        # 评分过滤
        if 'rating' in args and args['rating']:
            query_params['rating'] = args['rating']

        # 排序设置
        ordering = ['-is_top', '-review_time']  # 默认按置顶和时间倒序
        if 'ordering' in args and args['ordering']:
            ordering = args['ordering']
        query_params['ordering'] = ordering

        # 是否只查询有图评价
        if args.get('has_image'):
            reviews, total = self.repo.get_reviews_with_images(**query_params)
        else:
            reviews, total = self.repo.get_product_reviews(**query_params)

        # 获取评价统计数据
        stats = self.repo.get_review_count_by_rating(product_id)

        return dict(
            data=reviews,
            total=total,
            statistics=stats,
            code=200
        )

    def get_user_reviews(self, user_id: str) -> Dict[str, Any]:
        """
        获取用户的所有评价

        参数:
            user_id: 用户ID

        返回:
            包含用户评价列表的字典
        """
        reviews = self.repo.get_user_reviews(user_id)
        return dict(data=reviews, total=len(reviews), code=200)

    def get_order_reviews(self, order_no: str) -> Dict[str, Any]:
        """
        获取订单的所有评价

        参数:
            order_no: 订单编号

        返回:
            包含订单评价列表的字典
        """
        reviews = self.repo.get_order_reviews(order_no)
        return dict(data=reviews, total=len(reviews), code=200)

    def create_review(self, review_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建商品评价

        参数:
            review_data: 评价数据，包含以下字段:
                - order_no: 订单编号
                - order_detail_id: 订单详情ID
                - product_id: 商品ID
                - rating: 评分(1-5)
                - content: 评价内容
                - images: 评价图片URL列表
                - is_anonymous: 是否匿名评价

        返回:
            包含创建结果的字典
        """
        # 获取当前用户
        current_user = get_current_user()
        user_id = current_user.id

        # 验证订单是否存在且属于当前用户
        order_result = self.order_service.get_order_by_order_no(review_data.get('order_no'))
        if order_result.get('code') != 200 or not order_result.get('data'):
            return dict(code=404, message="订单不存在")

        order = order_result.get('data')
        if str(order.user_id) != str(user_id):
            return dict(code=403, message="无权评价该订单")

        # 验证订单状态是否允许评价
        if order.status != '已完成':
            return dict(code=400, message="订单未完成，不能评价")

        # 检查是否已经评价过
        existing_review = self.repo.find(
            order_no=review_data.get('order_no'),
            order_detail_id=review_data.get('order_detail_id')
        )
        if existing_review:
            return dict(code=400, message="该订单商品已评价，不能重复评价")

        # 处理图片数据
        images = review_data.get('images', [])
        if images and isinstance(images, list):
            review_data['images'] = json.dumps(images)
        elif images and isinstance(images, str):
            # 如果已经是JSON字符串，保持原样
            pass
        else:
            review_data['images'] = None

        # 设置评价数据
        review = OrderReview(
            order_no=review_data.get('order_no'),
            order_detail_id=review_data.get('order_detail_id'),
            product_id=review_data.get('product_id'),
            user_id=user_id,
            nickname=current_user.nickname if hasattr(current_user, 'nickname') else None,
            avatar=current_user.avatar if hasattr(current_user, 'avatar') else None,
            rating=review_data.get('rating', 5),
            content=review_data.get('content'),
            images=review_data.get('images'),
            is_anonymous=review_data.get('is_anonymous', False),
            status='已发布',  # 默认状态，可根据需要设置为审核中
            review_time=dt.datetime.now()
        )

        # 创建评价
        result = self.create(review)

        # 如果有统计表，可以在这里更新商品评价统计
        # self._update_product_review_stats(review.product_id)

        return dict(data=result, code=200, message="评价提交成功")

    def reply_review(self, review_id: int, reply_content: str) -> Dict[str, Any]:
        """
        商家回复评价

        参数:
            review_id: 评价ID
            reply_content: 回复内容

        返回:
            包含回复结果的字典
        """
        # 获取当前用户
        current_user = get_current_user()

        # 验证权限（这里简化处理，实际可能需要更复杂的权限验证）
        # if not has_permission(current_user, 'reply_review'):
        #     return dict(code=403, message="无权回复评价")

        # 回复评价
        result = self.repo.reply_review(
            review_id=review_id,
            reply_content=reply_content,
            replier=current_user.username if hasattr(current_user, 'username') else 'admin'
        )

        if not result:
            return dict(code=404, message="评价不存在")

        return dict(data=result, code=200, message="回复成功")

    def update_review_status(self, review_id: int, status: str) -> Dict[str, Any]:
        """
        更新评价状态

        参数:
            review_id: 评价ID
            status: 新状态(审核中/已发布/已屏蔽)

        返回:
            包含更新结果的字典
        """
        # 获取当前用户
        current_user = get_current_user()

        # 验证权限（这里简化处理）
        # if not has_permission(current_user, 'manage_review'):
        #     return dict(code=403, message="无权管理评价")

        # 更新状态
        result = self.repo.update_review_status(review_id, status)

        if not result:
            return dict(code=404, message="评价不存在")

        # 更新评价统计
        # self._update_product_review_stats(result.product_id)

        return dict(data=result, code=200, message=f"评价状态已更新为{status}")

    def set_top_status(self, review_id: int, is_top: bool) -> Dict[str, Any]:
        """
        设置评价置顶状态

        参数:
            review_id: 评价ID
            is_top: 是否置顶

        返回:
            包含更新结果的字典
        """
        # 获取当前用户
        current_user = get_current_user()

        # 验证权限（这里简化处理）
        # if not has_permission(current_user, 'manage_review'):
        #     return dict(code=403, message="无权管理评价")

        # 更新置顶状态
        result = self.repo.set_top_status(review_id, is_top)

        if not result:
            return dict(code=404, message="评价不存在")

        status_msg = "已置顶" if is_top else "已取消置顶"
        return dict(data=result, code=200, message=f"评价{status_msg}")

    def get_review_statistics(self, product_id: int) -> Dict[str, Any]:
        """
        获取商品评价统计数据

        参数:
            product_id: 商品ID

        返回:
            包含评价统计数据的字典
        """
        stats = self.repo.get_review_count_by_rating(product_id)
        return dict(data=stats, code=200)

    # 以下是可能需要的辅助方法

    def _update_product_review_stats(self, product_id: int) -> None:
        """
        更新商品评价统计数据

        参数:
            product_id: 商品ID
        """
        # 如果使用了汇总表，需要实现这个方法来更新统计数据
        # 这里省略实现，需要与OrderReviewSummary表配合使用
        pass

    def _get_client_ip(self) -> str:
        """获取客户端IP地址"""
        if not request:
            return ""

        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        elif request.headers.get('X-Real-IP'):
            return request.headers.get('X-Real-IP')
        else:
            return request.remote_addr or ""

    def _set_updater(self, entity: OrderReview) -> None:
        """设置更新者"""
        if hasattr(g, 'creator'):
            entity.updater = g.creator
        else:
            current_user = get_current_user()
            if hasattr(current_user, 'username'):
                entity.updater = current_user.username
