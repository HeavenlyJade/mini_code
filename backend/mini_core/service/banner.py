from typing import List, Optional, Dict, Any
from flask_jwt_extended import current_user, get_jwt_identity
from backend.mini_core.repository.banner.banner_sqla import BannerSQLARepository
from backend.mini_core.domain.banner import Banner
from kit.service.base import CRUDService
from kit.exceptions import ServiceBadRequest

__all__ = ['BannerService']


def _set_updater(banner: Banner) -> None:
    """设置更新者"""
    if hasattr(current_user, 'username') and current_user.username:
        banner.updater = current_user.username


def _set_creator(banner: Banner) -> None:
    """设置创建者"""
    if hasattr(current_user, 'username') and current_user.username:
        banner.creator = current_user.username


def _validate_banner(banner: Banner) -> None:
    """验证Banner数据"""
    if not banner.name:
        raise ServiceBadRequest("Banner名称不能为空")




class BannerService(CRUDService[Banner]):
    def __init__(self, repo: BannerSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> BannerSQLARepository:
        return self._repo

    def create(self, banner: Banner) -> Banner:
        """创建Banner"""
        _set_creator(banner)
        _validate_banner(banner)
        return super().create(banner)

    def batch_delete(self,ids: List[int]) -> None:
        return  self._repo.batch_delete(ids)
    def update(self, banner_id: int, banner: Banner) -> Optional[Banner]:
        """更新Banner"""
        _set_updater(banner)
        _validate_banner(banner)

        # 检查Banner是否存在
        existing_banner = self.get(banner_id)
        if not existing_banner:
            raise ServiceBadRequest("Banner不存在")
        return super().update(banner_id, banner)

    def update_status(self, banner_id: int, status: int) -> Optional[Banner]:
        """更新Banner状态"""
        if status not in [0, 1]:
            raise ServiceBadRequest("状态值无效，只能为0或1")

        banner = self.get(banner_id)
        if not banner:
            raise ServiceBadRequest("Banner不存在")

        # 如果状态没变，则不做更新
        if banner.status == status:
            return banner

        banner.status = status
        _set_updater(banner)

        return self.repo.update(banner_id, banner)

    def get_by_code_type(self, code_type: str, business_code: str = None) -> List[Banner]:
        """根据类型和业务编号获取Banner列表"""
        if not code_type:
            return []

        query_params = {'code_type': code_type, 'status': 1}
        if business_code:
            query_params['business_code'] = business_code

        banners = self.repo.find_all(**query_params)
        return sorted(banners, key=lambda x: (x.sort_order or 999))  # 处理sort_order为None的情况

