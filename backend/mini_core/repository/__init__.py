from backend.extensions import db

from .card.card_sqla import CardSQLARepository
from .distribution.distribution_sqla import (DistributionSQLARepository, DistributionConfigSQLARepository,
                                             DistributionGradeSQLARepository, DistributionGradeUpdateSQLARepository,
                                             DistributionIncomeSQLARepository, DistributionLogSQLARepository)
from .shop.shop_sqla import (ShopProductSQLARepository, ShopProductCategorySQLARepository)
from .shop.shop_specification import ShopSpecificationSQLARepository,ShopSpecificationAttributeSQLARepository
from .store.store_car_sqla import ShopStoreCategorySQLARepository
from .store.store_sqla import ShopStoreSQLARepository
from .order.order_sqla import ShopOrderSQLARepository
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


