# backend/mini_core/service/dashboard_service.py

import datetime as dt
from decimal import Decimal
from typing import Dict, Any

from sqlalchemy import func, and_

from backend.mini_core.domain.order.order import ShopOrder
from backend.mini_core.domain.order.order_return import OrderReturn
from backend.mini_core.domain.shop import ShopProduct
from backend.mini_core.domain.t_user import ShopUser
from .order.order import ShopOrderService
from .shop_user import ShopUserService
from .shop_server import  ShopProductService
from .order.order_return import OrderReturnService


class DashboardService:
    """仪表盘数据服务"""

    def __init__(self,
                 order_service: ShopOrderService,
                 user_service: ShopUserService,
                 product_service: ShopProductService,
                 return_service: OrderReturnService):
        self.order_service = order_service
        self.user_service = user_service
        self.product_service = product_service
        self.return_service = return_service

    def get_dashboard_data(self) -> Dict[str, Any]:
        """获取仪表盘所有数据"""

        # 获取当前时间
        now = dt.datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - dt.timedelta(days=1)

        # 获取各项统计数据
        core_metrics = self._get_core_metrics(today_start, yesterday_start)
        pending_tasks = self._get_pending_tasks()
        product_overview = self._get_product_overview()
        user_overview = self._get_user_overview()
        order_statistics = self._get_order_statistics(today_start)
        trend_data = self._get_trend_data()
        updated_at = now.isoformat()

        dashboard_data = {
            "core_metrics": core_metrics,
            "pending_tasks": pending_tasks,
            "product_overview": product_overview,
            "user_overview": user_overview,
            "order_statistics": order_statistics,
            "trend_data": trend_data,
            "updated_at": updated_at
        }

        return {"data": dashboard_data, "code": 200}

    def _get_core_metrics(self, today_start: dt.datetime, yesterday_start: dt.datetime) -> Dict[str, Any]:
        """获取核心指标数据"""
        # 通过service的repo属性获取session
        session = self.order_service.repo.session

        # 今日订单总数
        today_orders = session.query(func.count(ShopOrder.id)).filter(
            ShopOrder.create_time >= today_start
        ).scalar() or 0

        # 昨日订单总数
        yesterday_orders = session.query(func.count(ShopOrder.id)).filter(
            and_(
                ShopOrder.create_time >= yesterday_start,
                ShopOrder.create_time < today_start
            )
        ).scalar() or 0

        # 今日销售额
        today_sales = session.query(func.sum(ShopOrder.actual_amount)).filter(
            and_(
                ShopOrder.create_time >= today_start,
                ShopOrder.payment_status == '已支付'
            )
        ).scalar() or Decimal('0')

        # 昨日销售额
        yesterday_sales = session.query(func.sum(ShopOrder.actual_amount)).filter(
            and_(
                ShopOrder.create_time >= yesterday_start,
                ShopOrder.create_time < today_start,
                ShopOrder.payment_status == '已支付'
            )
        ).scalar() or Decimal('0')

        # 计算增长率
        order_growth = self._calculate_growth_rate(today_orders, yesterday_orders)
        sales_growth = self._calculate_growth_rate(float(today_sales), float(yesterday_sales))

        return {
            "today_orders": today_orders,
            "today_sales": float(today_sales),
            "yesterday_orders": yesterday_orders,
            "yesterday_sales": float(yesterday_sales),
            "order_growth_rate": order_growth,
            "sales_growth_rate": sales_growth
        }

    def _get_pending_tasks(self) -> Dict[str, Any]:
        """获取待处理事务数据"""
        order_session = self.order_service.repo.session
        return_session = self.return_service.repo.session
        product_session = self.product_service.repo.session

        # 待支付订单
        pending_payment = order_session.query(func.count(ShopOrder.id)).filter(
            ShopOrder.payment_status == '待支付'
        ).scalar() or 0

        # 待发货订单
        pending_shipment = order_session.query(func.count(ShopOrder.id)).filter(
            ShopOrder.delivery_status == '待发货'
        ).scalar() or 0

        # 待处理退货
        pending_returns = return_session.query(func.count(OrderReturn.id)).filter(
            OrderReturn.status == 0  # 待审核
        ).scalar() or 0

        # 库存不足商品
        low_stock_products = product_session.query(func.count(ShopProduct.id)).filter(
            and_(
                ShopProduct.stock <= ShopProduct.stock_alert,
                ShopProduct.stock_alert.isnot(None),
                ShopProduct.status == '上架'
            )
        ).scalar() or 0

        return {
            "pending_payment": pending_payment,
            "pending_shipment": pending_shipment,
            "pending_returns": pending_returns,
            "low_stock_products": low_stock_products
        }

    def _get_product_overview(self) -> Dict[str, Any]:
        """获取商品总览数据"""
        session = self.product_service.repo.session

        # 商品总数
        total_products = session.query(func.count(ShopProduct.id)).scalar() or 0

        # 上架商品
        online_products = session.query(func.count(ShopProduct.id)).filter(
            ShopProduct.status == '上架'
        ).scalar() or 0

        # 下架商品
        offline_products = session.query(func.count(ShopProduct.id)).filter(
            ShopProduct.status == '下架'
        ).scalar() or 0

        # 售罄商品
        out_of_stock = session.query(func.count(ShopProduct.id)).filter(
            ShopProduct.stock == 0
        ).scalar() or 0

        # 库存预警商品
        stock_warning = session.query(func.count(ShopProduct.id)).filter(
            and_(
                ShopProduct.stock <= ShopProduct.stock_alert,
                ShopProduct.stock_alert.isnot(None),
                ShopProduct.stock > 0
            )
        ).scalar() or 0

        return {
            "total": total_products,
            "online": online_products,
            "offline": offline_products,
            "out_of_stock": out_of_stock,
            "stock_warning": stock_warning
        }

    def _get_user_overview(self) -> Dict[str, Any]:
        """获取用户总览数据"""
        user_session = self.user_service.repo.session
        order_session = self.order_service.repo.session
        now = dt.datetime.now()

        # 用户总数
        total_users = user_session.query(func.count(ShopUser.id)).scalar() or 0

        # 今日新增用户
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_new_users = user_session.query(func.count(ShopUser.id)).filter(
            ShopUser.register_time >= today_start
        ).scalar() or 0

        # 本月新增用户
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_new_users = user_session.query(func.count(ShopUser.id)).filter(
            ShopUser.register_time >= month_start
        ).scalar() or 0

        # 活跃用户（本月有订单的用户）
        active_users = order_session.query(func.count(func.distinct(ShopOrder.user_id))).filter(
            ShopOrder.create_time >= month_start
        ).scalar() or 0

        return {
            "total": total_users,
            "today_new": today_new_users,
            "month_new": month_new_users,
            "active": active_users
        }

    def _get_order_statistics(self, today_start: dt.datetime) -> Dict[str, Any]:
        """获取订单统计数据"""
        session = self.order_service.repo.session

        # 今日订单金额统计
        today_amount_stats = session.query(
            func.sum(ShopOrder.actual_amount).label('total_amount'),
            func.avg(ShopOrder.actual_amount).label('avg_amount'),
            func.count(ShopOrder.id).label('order_count')
        ).filter(
            and_(
                ShopOrder.create_time >= today_start,
                ShopOrder.payment_status == '已支付'
            )
        ).first()

        # 本月订单金额统计
        month_start = today_start.replace(day=1)
        month_amount_stats = session.query(
            func.sum(ShopOrder.actual_amount).label('total_amount'),
            func.count(ShopOrder.id).label('order_count')
        ).filter(
            and_(
                ShopOrder.create_time >= month_start,
                ShopOrder.payment_status == '已支付'
            )
        ).first()

        return {
            "today": {
                "total_amount": float(today_amount_stats.total_amount or 0),
                "avg_amount": float(today_amount_stats.avg_amount or 0),
                "order_count": today_amount_stats.order_count or 0
            },
            "month": {
                "total_amount": float(month_amount_stats.total_amount or 0),
                "order_count": month_amount_stats.order_count or 0
            }
        }

    def _get_trend_data(self) -> Dict[str, Any]:
        """获取趋势数据（最近7天）"""
        session = self.order_service.repo.session

        # 获取最近7天的数据
        end_date = dt.datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        start_date = end_date - dt.timedelta(days=6)
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

        # 按天统计订单和销售额
        daily_stats = session.query(
            func.date(ShopOrder.create_time).label('date'),
            func.count(ShopOrder.id).label('order_count'),
            func.sum(ShopOrder.actual_amount).label('sales_amount')
        ).filter(
            and_(
                ShopOrder.create_time >= start_date,
                ShopOrder.create_time <= end_date,
                ShopOrder.payment_status == '已支付'
            )
        ).group_by(func.date(ShopOrder.create_time)).all()

        # 构建7天的完整数据
        trend_data = []
        for i in range(7):
            current_date = (start_date + dt.timedelta(days=i)).date()

            # 查找当天的数据
            day_data = next((stat for stat in daily_stats if stat.date == current_date), None)

            trend_data.append({
                "date": current_date.strftime('%Y-%m-%d'),
                "order_count": day_data.order_count if day_data else 0,
                "sales_amount": float(day_data.sales_amount or 0) if day_data else 0
            })

        return {
            "daily_trends": trend_data
        }

    def _calculate_growth_rate(self, current: float, previous: float) -> float:
        """计算增长率"""
        if previous == 0:
            return 100.0 if current > 0 else 0.0
        return round(((current - previous) / previous) * 100, 2)
