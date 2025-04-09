from backend.extensions import db

from .card.card_sqla import CardSQLARepository
from .distribution.distribution_sqla import (DistributionSQLARepository, DistributionConfigSQLARepository,
                                             DistributionGradeSQLARepository, DistributionGradeUpdateSQLARepository,
                                             DistributionIncomeSQLARepository, DistributionLogSQLARepository)

from .shop.shop_sqla import (ShopProductSQLARepository, ShopProductCategorySQLARepository)
from .shop.shop_specification import ShopSpecificationSQLARepository, ShopSpecificationAttributeSQLARepository
from .store.store_car_sqla import ShopStoreCategorySQLARepository
from .store.store_sqla import ShopStoreSQLARepository
from .order.order_sqla import ShopOrderSQLARepository
from .order.order_detail_sql import OrderDetailSQLARepository
from .order.order_log_sql import OrderLogSQLARepository
from .order.shop_order_setting_sqla import ShopOrderSettingSQLARepository
from .order.shop_return_reason_sqla import ShopReturnReasonSQLARepository
from .order.order_return_sql import OrderReturnSQLARepository, OrderReturnDetailSQLARepository, \
    OrderReturnLogSQLARepository
from .shop.shop_user_sqla import ShopUserSQLARepository, ShopUserAddressSQLARepository

# TODO replace this with DI
log_sqla_repo = CardSQLARepository(db.session)

# 分销
distribution_sqla_repo = DistributionSQLARepository(db.session)
distribution_config_sqla_repo = DistributionConfigSQLARepository(db.session)
distribution_grade_sqla_repo = DistributionGradeSQLARepository(db.session)
distribution_grade_update_sqla_repo = DistributionGradeUpdateSQLARepository(db.session)
distribution_income_sqla_repo = DistributionIncomeSQLARepository(db.session)
distribution_log_sqla_repo = DistributionLogSQLARepository(db.session)

# 商城
shop_product_sqla_repo = ShopProductSQLARepository(db.session)
shop_product_category_sqla_repo = ShopProductCategorySQLARepository(db.session)

# 门店
store_sqla_repo = ShopStoreSQLARepository(db.session)
store_sqla_category_repo = ShopStoreCategorySQLARepository(db.session)

# 规格尺寸
shop_specification_sqla_repo = ShopSpecificationSQLARepository(db.session)
shop_specification_attribute_sqla_repo = ShopSpecificationAttributeSQLARepository(db.session)

# 订单
shop_order_sqla_repo = ShopOrderSQLARepository(db.session)
shop_order_detail_sqla_repo = OrderDetailSQLARepository(db.session)
order_log_sqla_repo = OrderLogSQLARepository(db.session)
shop_order_setting_sqla_repo = ShopOrderSettingSQLARepository(db.session)
shop_return_reason_sqla_repo = ShopReturnReasonSQLARepository(db.session)
# 订单退货
shop_order_return_sqla_repo = OrderReturnSQLARepository(db.session)
shop_order_return_detail_sqla_repo = OrderReturnDetailSQLARepository(db.session)
shop_order_return_log_sqla_repo = OrderReturnLogSQLARepository(db.session)

# 商城用户
shop_user_sqla_repo = ShopUserSQLARepository(db.session)
shop_user_address_sqla_repo = ShopUserAddressSQLARepository(db.session)
