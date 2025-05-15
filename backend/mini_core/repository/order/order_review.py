import datetime as dt
from typing import Type, Tuple, List, Dict, Any
import json

from sqlalchemy import Column, String, Table, Integer, DateTime, Text, Boolean, BigInteger
from sqlalchemy import func, and_, or_, desc

from backend.extensions import mapper_registry
from backend.mini_core.domain.order.order_review import OrderReview
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column

__all__ = ['OrderReviewSQLARepository']

# 订单评价表
order_review_table = Table(
    'shop_order_review',
    mapper_registry.metadata,
    id_column(),
    Column('order_no', String(64), nullable=False, index=True, comment='订单编号'),
    Column('order_detail_id', String(64), nullable=False, index=True, comment='订单详情ID'),
    Column('product_id', Integer, nullable=False, index=True, comment='商品ID'),
    Column('user_id', String(32), nullable=False, index=True, comment='用户ID'),
    Column('nickname', String(64), comment='用户昵称'),
    Column('avatar', String(255), comment='用户头像'),
    Column('rating', Integer, nullable=False, default=5, comment='评分(1-5)'),
    Column('content', Text, comment='评价内容'),
    Column('images', Text, comment='评价图片(JSON字符串，存储图片URL列表)'),
    Column('is_anonymous', Boolean, default=False, comment='是否匿名评价'),
    Column('status', String(20), default='已发布', comment='评价状态(审核中/已发布/已屏蔽)'),
    Column('is_top', Boolean, default=False, comment='是否置顶'),
    Column('review_time', DateTime, nullable=False, default=dt.datetime.now, comment='评价时间'),
    Column('reply_content', Text, comment='商家回复内容'),
    Column('reply_time', DateTime, comment='商家回复时间'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
    Column('updater', String(64), comment='更新人'),
)

# 映射关系
mapper_registry.map_imperatively(OrderReview, order_review_table)


class OrderReviewSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[OrderReview]:
        return OrderReview

    @property
    def query_params(self) -> Tuple:
        return ('product_id', 'order_no', 'order_detail_id', 'user_id', 'status', 'rating', 'is_anonymous', 'is_top')

    @property
    def fuzzy_query_params(self) -> Tuple:
        return ('content', 'nickname')

    @property
    def range_query_params(self) -> Tuple:
        return ('review_time', 'reply_time', 'create_time')

    def get_product_reviews(self, product_id: int, **kwargs) -> Tuple[List[OrderReview], int]:
        """
        获取指定商品的评价列表

        参数:
            product_id: 商品ID
            **kwargs: 其他过滤条件

        返回:
            商品评价列表和总数
        """
        query_params = {'product_id': product_id, 'status': '已发布', **kwargs}

        # 处理排序
        ordering = kwargs.get('ordering', ['-is_top', '-review_time'])
        query_params['ordering'] = ordering

        # 执行查询
        return self.list(**query_params)

    def get_user_reviews(self, user_id: str) -> List[OrderReview]:
        """
        获取用户发表的所有评价

        参数:
            user_id: 用户ID

        返回:
            用户评价列表
        """
        return self.find_all(user_id=user_id)

    def get_order_reviews(self, order_no: str) -> List[OrderReview]:
        """
        获取订单的所有评价

        参数:
            order_no: 订单编号

        返回:
            订单评价列表
        """
        return self.find_all(order_no=order_no)

    def get_reviews_with_images(self, product_id: int, **kwargs) -> Tuple[List[OrderReview], int]:
        """
        获取带有图片的评价

        参数:
            product_id: 商品ID
            **kwargs: 其他过滤条件

        返回:
            带有图片的评价列表和总数
        """
        query_params = {'product_id': product_id, 'status': '已发布', **kwargs}
        conditions = self._get_conditions(**query_params)

        # 添加图片非空条件
        query = self.session.query(self.model).filter(*conditions).filter(
            self.model.images.isnot(None),
            self.model.images != '[]',
            self.model.images != ''
        )

        # 计算总数
        total = query.count() if kwargs.get('need_total_count', True) else 0

        # 排序
        ordering = kwargs.get('ordering', ['-is_top', '-review_time'])
        sort_conditions = self._get_sort_conditions(ordering=ordering)
        query = query.order_by(*sort_conditions)

        # 分页
        if 'page' in kwargs and 'size' in kwargs:
            query = self.and_pagination(query, kwargs['page'], kwargs['size'])

        return query.all(), total

    def update_review_status(self, review_id: int, status: str) -> OrderReview:
        """
        更新评价状态

        参数:
            review_id: 评价ID
            status: 新状态(审核中/已发布/已屏蔽)

        返回:
            更新后的评价对象
        """
        review = self.get_by_id(review_id)
        if review:
            review.status = status
            self.session.commit()
        return review

    def reply_review(self, review_id: int, reply_content: str, replier: str) -> OrderReview:
        """
        回复评价

        参数:
            review_id: 评价ID
            reply_content: 回复内容
            replier: 回复人

        返回:
            更新后的评价对象
        """
        review = self.get_by_id(review_id)
        if review:
            review.reply_content = reply_content
            review.reply_time = dt.datetime.now()
            review.updater = replier
            self.session.commit()
        return review

    def set_top_status(self, review_id: int, is_top: bool) -> OrderReview:
        """
        设置评价置顶状态

        参数:
            review_id: 评价ID
            is_top: 是否置顶

        返回:
            更新后的评价对象
        """
        review = self.get_by_id(review_id)
        if review:
            review.is_top = is_top
            self.session.commit()
        return review

    def get_review_count_by_rating(self, product_id: int) -> Dict[str, int]:
        """
        获取商品各评分数量统计

        参数:
            product_id: 商品ID

        返回:
            各评分数量统计字典
        """
        stats = {}

        # 查询评分统计
        for rating in range(1, 6):
            count = self.session.query(func.count(self.model.id)).filter(
                self.model.product_id == product_id,
                self.model.rating == rating,
                self.model.status == '已发布'
            ).scalar() or 0
            stats[f'rating_{rating}'] = count

        # 查询总评价数
        stats['total'] = sum(stats.values())

        # 计算好评、中评、差评数
        stats['good'] = stats.get('rating_4', 0) + stats.get('rating_5', 0)
        stats['mid'] = stats.get('rating_3', 0)
        stats['bad'] = stats.get('rating_1', 0) + stats.get('rating_2', 0)

        # 计算有图评价数
        stats['with_images'] = self.session.query(func.count(self.model.id)).filter(
            self.model.product_id == product_id,
            self.model.status == '已发布',
            self.model.images.isnot(None),
            self.model.images != '[]',
            self.model.images != ''
        ).scalar() or 0

        # 计算平均评分
        if stats['total'] > 0:
            avg_rating = (
                             stats.get('rating_1', 0) * 1 +
                             stats.get('rating_2', 0) * 2 +
                             stats.get('rating_3', 0) * 3 +
                             stats.get('rating_4', 0) * 4 +
                             stats.get('rating_5', 0) * 5
                         ) / stats['total']
            stats['avg_rating'] = round(avg_rating, 1)
        else:
            stats['avg_rating'] = 5.0

        return stats
