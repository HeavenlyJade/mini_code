from marshmallow import validate, Schema, validates, ValidationError
from marshmallow_dataclass import class_schema
from webargs import fields as webargs_fields

from backend.mini_core.domain.order.order_review import OrderReview
from kit.schema.base import EntitySchema, ListResultSchema, ListQueryArgSchema
from kit.schema.field import DateTimeDelimitedList


# 基本 Schema 类 - 使用 class_schema 自动生成
OrderReviewSchema = class_schema(OrderReview, base_schema=EntitySchema)


# 评价查询参数 Schema
class OrderReviewQueryArgSchema(ListQueryArgSchema):
    product_id = webargs_fields.Int(description='商品ID')
    order_no = webargs_fields.Str(description='订单编号')
    order_detail_id = webargs_fields.Str(description='订单详情ID')
    user_id = webargs_fields.Str(description='用户ID')
    rating = webargs_fields.Int(description='评分(1-5)', validate=validate.Range(min=1, max=5))
    has_image = webargs_fields.Bool(description='是否只查看有图评价')
    status = webargs_fields.Str(description='评价状态(审核中/已发布/已屏蔽)')
    is_anonymous = webargs_fields.Bool(description='是否匿名评价')
    is_top = webargs_fields.Bool(description='是否置顶')
    review_time = DateTimeDelimitedList(description='评价时间范围')
    content_keyword = webargs_fields.Str(description='评价内容关键词')


# 评价创建参数 Schema
class OrderReviewCreateSchema(Schema):
    order_no = webargs_fields.Str(required=True, description='订单编号')
    order_detail_id = webargs_fields.Str(required=True, description='订单详情ID')
    product_id = webargs_fields.Int(required=True, description='商品ID')
    rating = webargs_fields.Int(required=True, description='评分(1-5)', validate=validate.Range(min=1, max=5))
    content = webargs_fields.Str(description='评价内容')
    images = webargs_fields.List(webargs_fields.Str(), description='评价图片URL列表')
    is_anonymous = webargs_fields.Bool(missing=False, description='是否匿名评价')

    @validates('content')
    def validate_content(self, value):
        if not value or len(value.strip()) == 0:
            raise ValidationError('评价内容不能为空')
        if len(value) > 500:
            raise ValidationError('评价内容不能超过500个字符')


# 评价回复参数 Schema
class OrderReviewReplySchema(Schema):
    review_id = webargs_fields.Int(required=True, description='评价ID')
    reply_content = webargs_fields.Str(required=True, description='回复内容')

    @validates('reply_content')
    def validate_reply_content(self, value):
        if not value or len(value.strip()) == 0:
            raise ValidationError('回复内容不能为空')
        if len(value) > 500:
            raise ValidationError('回复内容不能超过500个字符')


# 评价状态更新参数 Schema
class OrderReviewStatusUpdateSchema(Schema):
    review_id = webargs_fields.Int(required=True, description='评价ID')
    status = webargs_fields.Str(required=True, description='评价状态',
                              validate=validate.OneOf(['审核中', '已发布', '已屏蔽']))


# 评价置顶参数 Schema
class OrderReviewTopUpdateSchema(Schema):
    review_id = webargs_fields.Int(required=True, description='评价ID')
    is_top = webargs_fields.Bool(required=True, description='是否置顶')


# 单条评价统计 Schema
class ReviewStatItemSchema(Schema):
    rating = webargs_fields.Int(description='评分')
    count = webargs_fields.Int(description='数量')
    percentage = webargs_fields.Float(description='百分比')


# 评价统计 Schema
class OrderReviewStatsSchema(Schema):
    total = webargs_fields.Int(description='总评价数')
    avg_rating = webargs_fields.Float(description='平均评分')
    rating_1 = webargs_fields.Int(description='1星评价数')
    rating_2 = webargs_fields.Int(description='2星评价数')
    rating_3 = webargs_fields.Int(description='3星评价数')
    rating_4 = webargs_fields.Int(description='4星评价数')
    rating_5 = webargs_fields.Int(description='5星评价数')
    good = webargs_fields.Int(description='好评数(4-5星)')
    mid = webargs_fields.Int(description='中评数(3星)')
    bad = webargs_fields.Int(description='差评数(1-2星)')
    with_images = webargs_fields.Int(description='有图评价数')
    rating_detail = webargs_fields.List(webargs_fields.Nested(ReviewStatItemSchema), description='各评分详情')


# 响应 Schema
class OrderReviewResponseSchema(Schema):
    data = webargs_fields.Nested(OrderReviewSchema)
    code = webargs_fields.Int(description='状态码')
    message = webargs_fields.Str(description='消息')


class OrderReviewListResponseSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(OrderReviewSchema))
    statistics = webargs_fields.Nested(OrderReviewStatsSchema, description='评价统计')
    code = webargs_fields.Int(description='状态码')
    total = webargs_fields.Int(description='总数')


class OrderReviewStatsResponseSchema(Schema):
    data = webargs_fields.Nested(OrderReviewStatsSchema)
    code = webargs_fields.Int(description='状态码')
