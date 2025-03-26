from backend.extensions import db

from .card.card_sqla import CardSQLARepository
from .distribution.distribution_sqla import (DistributionSQLARepository, DistributionConfigSQLARepository,
                                             DistributionGradeSQLARepository, DistributionGradeUpdateSQLARepository,
                                             DistributionIncomeSQLARepository, DistributionLogSQLARepository)
from .shop.shop_sqla import (ShopProductSQLARepository, ShopProductCategorySQLARepository)
from .store.store_car_sqla import ShopStoreCategorySQLARepository
from .store.store_sqla import ShopStoreSQLARepository
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

