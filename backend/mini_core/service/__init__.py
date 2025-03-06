from backend.mini_core.repository import (log_sqla_repo,distribution_sqla_repo,
                                          distribution_config_sqla_repo,
                                          distribution_grade_sqla_repo,distribution_grade_update_sqla_repo,
                                          distribution_income_sqla_repo,distribution_log_sqla_repo)
from .card_server import CardService
from .distribution_server import (DistributionService,DistributionConfigService,DistributionGradeService,
                                  DistributionGradeUpdateService,DistributionIncomeService,DistributionLogService)

card_service = CardService(log_sqla_repo)

distribution_service = DistributionService(distribution_sqla_repo)
distribution_config_service = DistributionConfigService(distribution_config_sqla_repo)
distribution_grade_service = DistributionGradeService(distribution_grade_sqla_repo,distribution_grade_update_sqla_repo)
distribution_grade_update_service = DistributionGradeUpdateService(distribution_grade_update_sqla_repo)
distribution_income_service = DistributionIncomeService(distribution_income_sqla_repo)
distribution_log_service = DistributionLogService(distribution_log_sqla_repo)
