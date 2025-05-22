from backend.mini_core.repository import (log_sqla_repo, distribution_sqla_repo,
                                          distribution_config_sqla_repo,
                                          distribution_grade_sqla_repo, distribution_grade_update_sqla_repo,
                                          distribution_income_sqla_repo, distribution_log_sqla_repo,
                                          shop_product_sqla_repo, shop_product_category_sqla_repo,
                                          store_sqla_repo, store_sqla_category_repo,
                                          shop_specification_attribute_sqla_repo, shop_specification_sqla_repo,
                                          shop_order_sqla_repo, shop_order_detail_sqla_repo, order_log_sqla_repo,
                                          shop_order_setting_sqla_repo, shop_return_reason_sqla_repo,
                                          shop_user_sqla_repo, shop_user_address_sqla_repo,
                                          shop_order_return_sqla_repo, shop_order_return_detail_sqla_repo,
                                          shop_order_return_log_sqla_repo,banner_sqla_repo,shop_order_cart_sqla_repo,
                                          shop_order_logistics_sqla_repo,
                                          shop_order_review_repo)
from .card_server import CardService
from .distribution_server import (DistributionService, DistributionConfigService,
                                  DistributionGradeService, DistributionGradeUpdateService,
                                  DistributionIncomeService, DistributionLogService)
from .order.order import ShopOrderService
from .order.order_detail import OrderDetailService
from .order.order_log import OrderLogService
from .order.order_return import OrderReturnService, OrderReturnDetailService, OrderReturnLogService
from .order.shop_order_setting import ShopOrderSettingService
from .order.shop_return_reason import ShopReturnReasonService
from .shop_server import (ShopProductCategoryService, ShopProductService)
from .shop_specification import ShopSpecificationService, ShopSpecificationAttributeService
from .shop_user import ShopUserService, ShopUserAddressService
from .store import (ShopStoreCategoryService, ShopStoreService)
from .banner import BannerService
from .order.shop_order_cart import ShopOrderCartService
from .order.shop_order_logistics import ShopOrderLogisticsService
from .order.order_review import OrderReviewService
from .dashboard import DashboardService
# 个人卡牌
card_service = CardService(log_sqla_repo)
# 分销系统
distribution_service = DistributionService(distribution_sqla_repo)
distribution_config_service = DistributionConfigService(distribution_config_sqla_repo)
distribution_grade_service = DistributionGradeService(distribution_grade_sqla_repo, distribution_grade_update_sqla_repo)
distribution_grade_update_service = DistributionGradeUpdateService(distribution_grade_update_sqla_repo)
distribution_income_service = DistributionIncomeService(distribution_income_sqla_repo)
distribution_log_service = DistributionLogService(distribution_log_sqla_repo)
# 商品系统

shop_product_service = ShopProductService(shop_product_sqla_repo)
shop_product_category_service = ShopProductCategoryService(shop_product_category_sqla_repo)

# 门店管理
shop_store_service = ShopStoreService(store_sqla_repo)
shop_store_category_service = ShopStoreCategoryService(store_sqla_category_repo)

shop_specification_service = ShopSpecificationService(shop_specification_sqla_repo,
                                                      shop_specification_attribute_sqla_repo)
shop_specification_attribute_service = ShopSpecificationAttributeService(shop_specification_attribute_sqla_repo)

# 订单
shop_order_service = ShopOrderService(shop_order_sqla_repo)
order_detail_service = OrderDetailService(shop_order_detail_sqla_repo)
order_log_service = OrderLogService(order_log_sqla_repo)
shop_order_setting_service = ShopOrderSettingService(shop_order_setting_sqla_repo)
shop_return_reason_service = ShopReturnReasonService(shop_return_reason_sqla_repo)

# 订单退货
order_return_service = OrderReturnService(shop_order_return_sqla_repo, shop_order_return_detail_sqla_repo,
                                          shop_order_return_log_sqla_repo)
order_return_detail_service = OrderReturnDetailService(shop_order_return_detail_sqla_repo)
order_return_log_service = OrderReturnLogService(shop_order_return_log_sqla_repo)
# 商城用户
shop_user_service = ShopUserService(shop_user_sqla_repo)
shop_user_address_service = ShopUserAddressService(shop_user_address_sqla_repo)
banner_service = BannerService(banner_sqla_repo)

shop_order_cart_service = ShopOrderCartService(shop_order_cart_sqla_repo)
# 订单的物流服务
shop_order_logistics_service = ShopOrderLogisticsService(shop_order_logistics_sqla_repo)
order_review_service = OrderReviewService(shop_order_review_repo)

# 仪表盘
# 创建仪表盘服务实例
dashboard_service = DashboardService(order_service=shop_order_service,
    user_service=shop_user_service,
    product_service=shop_product_service,
    return_service=order_return_service
)
