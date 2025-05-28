from dataclasses import field
from typing import Optional, List,Dict,Any
from decimal import Decimal
from datetime import datetime
from marshmallow_dataclass import dataclass

from kit.domain.entity import Entity


@dataclass
class OrderReturn(Entity):
    """
    订单退货领域模型

    用于表示用户的退货/退款申请信息，包括退货单号、关联订单、退款金额、状态等
    """
    return_no: str = field(
        default=None,
        metadata=dict(
            description='退货单号',
        ),
    )
    order_no: str = field(
        default=None,
        metadata=dict(
            description='关联订单编号',
        ),
    )
    user_id: str = field(
        default=None,
        metadata=dict(
            description='用户ID',
        ),
    )
    return_type: str = field(
        default=None,
        metadata=dict(
            description='退货类型(退货退款/仅退款)',
        ),
    )
    return_reason_id: int = field(
        default=None,
        metadata=dict(
            description='退货原因ID',
        ),
    )
    return_reason: str = field(
        default=None,
        metadata=dict(
            description='退货原因描述',
        ),
    )
    return_amount: Decimal = field(
        default=None,
        metadata=dict(
            description='退款金额',
        ),
    )
    return_quantity: int = field(
        default=None,
        metadata=dict(
            description='退货数量',
        ),
    )
    status: int = field(
        default=None,
        metadata=dict(
            description='退货状态(0待审核/1已同意/2已拒绝/3退款中/4已完成)',
        ),
    )
    refuse_reason: str = field(
        default=None,
        metadata=dict(
            description='拒绝原因',
        ),
    )
    apply_time: datetime = field(
        default=None,
        metadata=dict(
            description='申请时间',
        ),
    )
    audit_time: datetime = field(
        default=None,
        metadata=dict(
            description='审核时间',
        ),
    )
    complete_time: datetime = field(
        default=None,
        metadata=dict(
            description='完成时间',
        ),
    )
    return_express_company: str = field(
        default=None,
        metadata=dict(
            description='退货快递公司',
        ),
    )
    return_express_no: str = field(
        default=None,
        metadata=dict(
            description='退货快递单号',
        ),
    )
    images: str = field(
        default=None,
        metadata=dict(
            description='图片凭证(JSON格式)',
        ),
    )
    description: str = field(
        default=None,
        metadata=dict(
            description='问题描述',
        ),
    )
    refund_way: str = field(
        default=None,
        metadata=dict(
            description='退款方式',
        ),
    )
    refund_account: str = field(
        default=None,
        metadata=dict(
            description='退款账号',
        ),
    )
    admin_remark: str = field(
        default=None,
        metadata=dict(
            description='管理员备注',
        ),
    )
    process_user_id: int = field(
        default=None,
        metadata=dict(
            description='处理人ID',
        ),
    )
    process_username: str = field(
        default=None,
        metadata=dict(
            description='处理人用户名',
        ),
    )
    updater: str = field(
        default=None,
        metadata=dict(
            description='更新人',
        ),
    )
    refund_points: int = field(
        default=0,
        metadata=dict(
            description='退还积分数量',
        ),
    )
    calculation_detail: Optional[Dict[str, Any]] = field(
        default=None,
        metadata=dict(
            description='退款计算明细(JSON格式)',
        ),
    )


@dataclass
class OrderReturnDetail(Entity):
    """
    订单退货商品明细领域模型

    用于表示退货单中的商品明细信息，包括商品ID、名称、数量、金额等
    """
    return_no: str = field(
        default=None,
        metadata=dict(
            description='关联订单编号',
        ),
    )
    order_item_id: str = field(
        default=None,
        metadata=dict(
            description='订单明细ID',
        ),
    )
    order_no: str = field(
        default=None,
        metadata=dict(
            description='订单ID',
        ),
    )
    product_id: int = field(
        default=None,
        metadata=dict(
            description='商品ID',
        ),
    )
    sku_id: str = field(
        default=None,
        metadata=dict(
            description='SKU ID',
        ),
    )
    product_name: str = field(
        default=None,
        metadata=dict(
            description='商品名称',
        ),
    )
    product_img: str = field(
        default=None,
        metadata=dict(
            description='商品图片',
        ),
    )
    product_spec: str = field(
        default=None,
        metadata=dict(
            description='商品规格',
        ),
    )
    price: Decimal = field(
        default=None,
        metadata=dict(
            description='商品单价',
        ),
    )
    quantity: int = field(
        default=None,
        metadata=dict(
            description='退货数量',
        ),
    )
    subtotal: Decimal = field(
        default=None,
        metadata=dict(
            description='小计金额',
        ),
    )
    reason: str = field(
        default=None,
        metadata=dict(
            description='该商品退货原因',
        ),
    )
    allocated_discount: Decimal = field(
        default=Decimal('0'),
        metadata=dict(
            description='该商品分摊的折扣金额',
        ),
    )
    allocated_points: Decimal = field(
        default=Decimal('0'),
        metadata=dict(
            description='该商品分摊的积分金额',
        ),
    )
    proportion: Decimal = field(
        default=Decimal('0'),
        metadata=dict(
            description='该商品在订单中的价格占比',
        ),
    )
    cash_refund_amount: Decimal = field(
        default=Decimal('0'),
        metadata=dict(
            description='现金退款金额',
        ),
    )
    points_refund_amount: int = field(
        default=0,
        metadata=dict(
            description='积分退款数量',
        ),
    )


@dataclass
class OrderReturnLog(Entity):
    """
    退货流程日志领域模型

    用于记录退货单的流程变更记录，包括操作类型、描述、操作人、时间等
    """
    return_no: str = field(
        default=None,
        metadata=dict(
            description='退货单号',
        ),
    )
    operation_type: str = field(
        default=None,
        metadata=dict(
            description='操作类型',
        ),
    )
    operation_desc: str = field(
        default=None,
        metadata=dict(
            description='操作描述',
        ),
    )
    operator: str = field(
        default=None,
        metadata=dict(
            description='操作人',
        ),
    )
    operation_time: datetime = field(
        default=None,
        metadata=dict(
            description='操作时间',
        ),
    )
    operation_ip: str = field(
        default=None,
        metadata=dict(
            description='操作IP',
        ),
    )
    old_status: str = field(
        default=None,
        metadata=dict(
            description='旧状态',
        ),
    )
    new_status: str = field(
        default=None,
        metadata=dict(
            description='新状态',
        ),
    )
    remark: str = field(
        default=None,
        metadata=dict(
            description='备注',
        ),
    )
