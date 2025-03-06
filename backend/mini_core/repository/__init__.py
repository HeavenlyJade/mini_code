from backend.extensions import db

from .card.card_sqla import CardSQLARepository
from .distribution.distribution_sqla import (DistributionSQLARepository, DistributionConfigSQLARepository,
                                             DistributionGradeSQLARepository, DistributionGradeUpdateSQLARepository,
                                             DistributionIncomeSQLARepository, DistributionLogSQLARepository)

# TODO replace this with DI
log_sqla_repo = CardSQLARepository(db.session)

# Distribution-related repository instances
distribution_sqla_repo = DistributionSQLARepository(db.session)
distribution_config_sqla_repo = DistributionConfigSQLARepository(db.session)
distribution_grade_sqla_repo = DistributionGradeSQLARepository(db.session)
distribution_grade_update_sqla_repo = DistributionGradeUpdateSQLARepository(db.session)
distribution_income_sqla_repo = DistributionIncomeSQLARepository(db.session)
distribution_log_sqla_repo = DistributionLogSQLARepository(db.session)
