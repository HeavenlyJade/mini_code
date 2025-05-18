from typing import Type, Tuple, List, Dict, Any, Union
import datetime as dt

from sqlalchemy import Column, String, Table, Integer, DateTime, Text, Enum, Boolean, Numeric, DECIMAL, BigInteger
from sqlalchemy import func, and_, or_, desc

from backend.extensions import mapper_registry
from backend.mini_core.domain.order.order_return import OrderReturn, OrderReturnDetail, OrderReturnLog
from kit.domain.entity import Entity, EntityInt
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column, JsonText

__all__ = ['OrderReturnSQLARepository', 'OrderReturnDetailSQLARepository', 'OrderReturnLogSQLARepository']

# 订单退货表
order_return_table = Table(
    'shop_order_return',
    mapper_registry.metadata,
    id_column(),
    Column('return_no', String(64), nullable=False, unique=True, comment='退货单号'),
    Column('order_no', String(64), nullable=False, comment='关联订单编号'),
    Column('user_id', BigInteger, nullable=False, comment='用户ID'),
    Column('return_type', String(32), nullable=False, comment='退货类型(退货退款/仅退款)'),
    Column('return_reason_id', Integer, comment='退货原因ID'),
    Column('return_reason', String(255), comment='退货原因描述'),
    Column('return_amount', DECIMAL(10, 2), default=0, comment='退款金额'),
    Column('return_quantity', Integer, default=0, comment='退货数量'),
    Column('status', Integer, comment='退货状态(0待审核/1已同意/2已拒绝/3退款中/4已完成)'),
    Column('refuse_reason', String(255), comment='拒绝原因'),
    Column('apply_time', DateTime, comment='申请时间'),
    Column('audit_time', DateTime, comment='审核时间'),
    Column('complete_time', DateTime, comment='完成时间'),
    Column('return_express_company', String(64), comment='退货快递公司'),
    Column('return_express_no', String(64), comment='退货快递单号'),
    Column('images', Text, comment='图片凭证(JSON格式)'),
    Column('description', Text, comment='问题描述'),
    Column('refund_way', String(32), comment='退款方式'),
    Column('refund_account', String(64), comment='退款账号'),
    Column('admin_remark', String(255), comment='管理员备注'),
    Column('process_user_id', BigInteger, comment='处理人ID'),
    Column('process_username', String(64), comment='处理人用户名'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
    Column('updater', String(64), comment='更新人'),
)

# 订单退货商品明细表
order_return_detail_table = Table(
    'shop_order_return_detail',
    mapper_registry.metadata,
    id_column(),
    Column('return_no', String(255), nullable=False, comment='退货单号'),
    Column('order_item_id', String(255), nullable=False, comment='订单明细ID'),
    Column('order_no', String(255), nullable=False, index=True, comment='订单ID'),
    Column('product_id', Integer, nullable=False, comment='商品ID'),
    Column('sku_id', String(64), comment='SKU ID'),
    Column('product_name', String(255), nullable=False, comment='商品名称'),
    Column('product_img', String(255), comment='商品图片'),
    Column('product_spec', String(255), comment='商品规格'),
    Column('price', DECIMAL(10, 2), nullable=False, comment='商品单价'),
    Column('quantity', Integer, nullable=False, comment='退货数量'),
    Column('subtotal', DECIMAL(10, 2), nullable=False, comment='小计金额'),
    Column('reason', String(255), comment='该商品退货原因'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
)

# 退货流程日志表
order_return_log_table = Table(
    'shop_order_return_log',
    mapper_registry.metadata,
    id_column(),
    Column('return_no', String(64), nullable=False, comment='退货单号'),
    Column('operation_type', String(32), nullable=False, comment='操作类型'),
    Column('operation_desc', String(255), nullable=False, comment='操作描述'),
    Column('operator', String(64), nullable=False, comment='操作人'),
    Column('operation_time', DateTime, nullable=False, comment='操作时间'),
    Column('operation_ip', String(64), comment='操作IP'),
    Column('old_status', String(32), comment='旧状态'),
    Column('new_status', String(32), comment='新状态'),
    Column('remark', String(255), comment='备注'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
)

# 映射关系
mapper_registry.map_imperatively(OrderReturn, order_return_table)
mapper_registry.map_imperatively(OrderReturnDetail, order_return_detail_table)
mapper_registry.map_imperatively(OrderReturnLog, order_return_log_table)


class OrderReturnSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[OrderReturn]:
        return OrderReturn

    @property
    def query_params(self) -> Tuple:
        return 'return_no', 'order_no', 'user_id', 'return_type', 'status', 'return_reason_id'

    @property
    def fuzzy_query_params(self) -> Tuple:
        return 'return_reason', 'return_express_no', 'description', 'process_username'

    @property
    def range_query_params(self) -> Tuple:
        return 'apply_time', 'audit_time', 'complete_time', 'return_amount'

    def get_return_stats(self) -> Dict[str, Any]:
        """获取退货统计信息"""
        total = self.query().count()
        pending_audit = self.query().filter(OrderReturn.status == '待审核').count()
        approved = self.query().filter(OrderReturn.status == '已同意').count()
        rejected = self.query().filter(OrderReturn.status == '已拒绝').count()
        in_refund = self.query().filter(OrderReturn.status == '退款中').count()
        completed = self.query().filter(OrderReturn.status == '已完成').count()

        # 今日退货申请数
        today_start = dt.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_returns = self.query().filter(OrderReturn.apply_time >= today_start).count()

        # 今日退款金额
        today_refund = self.session.query(func.sum(OrderReturn.return_amount)).filter(
            OrderReturn.apply_time >= today_start,
            OrderReturn.status == '已完成'
        ).scalar() or 0

        # 各退货类型统计
        type_stats = self.session.query(
            OrderReturn.return_type,
            func.count(OrderReturn.id).label('count')
        ).group_by(OrderReturn.return_type).all()

        return {
            'total': total,
            'pending_audit': pending_audit,
            'approved': approved,
            'rejected': rejected,
            'in_refund': in_refund,
            'completed': completed,
            'today_returns': today_returns,
            'today_refund': float(today_refund),
            'type_stats': [{'type': t[0], 'count': t[1]} for t in type_stats]
        }

    def get_user_returns(self, user_id: int) -> List[OrderReturn]:
        """获取用户的所有退货单"""
        return self.find_all(user_id=user_id)

    def get_by_return_no(self, return_no: str) -> OrderReturn:
        """通过退货单号获取退货单"""
        return self.find(return_no=return_no)

    def get_by_order_no(self, order_no: str) -> List[OrderReturn]:
        """通过订单号获取相关的退货单"""
        return self.find_all(order_no=order_no)

    def update_status(self, order_no:str, status: str, **kwargs) -> Type[Union[Entity, EntityInt]]:
        """更新退货单状态"""
        return_obj = self.find(order_no=order_no)
        if return_obj:
            return_obj.status = status

            # 根据状态更新相关时间
            if status == '已同意' or status == '已拒绝':
                return_obj.audit_time = dt.datetime.now()
            elif status == '已完成':
                return_obj.complete_time = dt.datetime.now()

            # 更新其他字段
            for key, value in kwargs.items():
                if hasattr(return_obj, key):
                    setattr(return_obj, key, value)
            self.session.commit()
        return return_obj

    def get_monthly_stats(self) -> List[Dict[str, Any]]:
        """获取按月统计的退货退款数据"""
        query = """
        SELECT DATE_FORMAT(apply_time, '%Y-%m') as month,
               COUNT(id) as return_count,
               SUM(return_amount) as total_refund
        FROM shop_order_return
        WHERE status = '已完成'
        GROUP BY DATE_FORMAT(apply_time, '%Y-%m')
        ORDER BY month DESC
        LIMIT 12
        """
        result = self.session.execute(query).fetchall()
        return [{'month': r[0], 'return_count': r[1], 'total_refund': float(r[2])} for r in result]

    def query(self):
        return self.session

    def create_return_transaction(self, return_data: dict, detail_items: list, order_no: str, username: str) -> Dict[
        str, Any]:
        """
        创建退货单及所有相关数据的事务操作

        将退货单创建、退货明细创建、订单状态更新等操作包含在一个事务中
        日志操作将被分离出来，由调用方单独处理

        参数:
            return_data: 退货单数据
            detail_items: 退货明细数据列表
            order_no: 订单编号
            username: 操作用户名

        返回:
            Dict: 包含操作结果的字典
        """
        from backend.mini_core.domain.order.order import ShopOrder
        from backend.mini_core.domain.order.order_detail import OrderDetail
        from sqlalchemy.exc import SQLAlchemyError
        from dataclasses import asdict
        # 获取当前时间
        now = dt.datetime.now()
        try:
            # 1. 创建退货单
            return_obj = OrderReturn(**return_data)
            self.session.add(return_obj)
            self.session.flush()  # 获取ID

            return_id = return_obj.id
            return_no = return_obj.return_no

            # 2. 创建退货商品明细
            detail_objects = []
            for item in detail_items:
                item_copy = item.copy()  # 创建副本，避免修改原始数据
                item_copy['return_no'] = return_no  # 设置退货单号
                detail_obj = OrderReturnDetail(**item_copy)
                self.session.add(detail_obj)
                detail_objects.append(asdict(detail_obj))

            # 3. 更新订单状态
            order = self.session.query(ShopOrder).filter(ShopOrder.order_no == order_no).first()
            if order:
                order.status = "退款中"
                order.refund_status = "退货中"
                order.updater = username

            # 4. 更新订单明细的退款状态
            for item in detail_items:
                order_item_id = item.get('order_item_id')
                # 找到对应的订单明细并更新状态
                detail = self.session.query(OrderDetail).filter(
                    OrderDetail.order_no == order_no,
                    OrderDetail.order_item_id == order_item_id
                ).first()

                if detail:
                    detail.refund_status = 1  # 设置为退款中状态
                    detail.refund_time = now

            # 提交事务
            self.session.commit()

            # 返回成功结果和创建的退货单对象，以便外部处理日志
            return dict(
                order=asdict(order),
                code=200,
                message="退货申请提交成功，等待商家审核",
                return_id=return_id,
                return_no=return_no,
            )

        except SQLAlchemyError as e:
            # 发生异常时回滚事务
            self.session.rollback()
            return dict(code=500, message=f"退货申请提交失败: {str(e)}")

class OrderReturnDetailSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[OrderReturnDetail]:
        return OrderReturnDetail

    @property
    def query_params(self) -> Tuple:
        return 'return_no', 'order_detail_id', 'product_id', 'sku_id',"order_no"

    @property
    def fuzzy_query_params(self) -> Tuple:
        return 'product_name', 'reason'

    def get_return_details(self, order_no: str) -> list[Entity]:
        """获取订单好的所有商品明细"""
        return self.find_all(order_no=order_no)

    def get_product_returns(self, product_id: int) -> list[Entity]:
        """获取指定商品的所有退货记录"""
        return self.find_all(product_id=product_id)

    def create_details(self, details: List[OrderReturnDetail]) -> None:
        """批量创建退货商品明细"""
        self.create_many(details)


class OrderReturnLogSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[OrderReturnLog]:
        return OrderReturnLog

    @property
    def query_params(self) -> Tuple:
        return 'return_no', 'return_no', 'operation_type'

    @property
    def fuzzy_query_params(self) -> Tuple:
        return 'operation_desc', 'operator', 'remark'

    @property
    def range_query_params(self) -> Tuple:
        return 'operation_time', 'create_time'

    def get_return_logs(self, return_no: str) -> List[OrderReturnLog]:
        """获取退货单的所有操作日志"""
        return self.get_base_queryset.filter(OrderReturnLog.return_no == return_no).order_by(
            desc(OrderReturnLog.operation_time)).all()

    def get_return_logs_by_no(self, return_no: str) -> List[OrderReturnLog]:
        """通过退货单号获取所有操作日志"""
        return self.session.query().filter(OrderReturnLog.return_no == return_no).order_by(
            desc(OrderReturnLog.operation_time)).all()

    def get_operator_logs(self, operator: str) -> List[OrderReturnLog]:
        """获取指定操作员的所有操作日志"""
        return self.session.query().filter(OrderReturnLog.operator == operator).order_by(
            desc(OrderReturnLog.operation_time)).all()

