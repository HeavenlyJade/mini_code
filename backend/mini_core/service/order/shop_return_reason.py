from typing import Optional, List, Dict, Any
from flask_jwt_extended import get_current_user
from kit.service.base import CRUDService
from backend.mini_core.domain.order.shop_return_reason import ShopReturnReason
from backend.mini_core.repository.order.shop_return_reason_sqla import ShopReturnReasonSQLARepository

__all__ = ['ShopReturnReasonService']


class ShopReturnReasonService(CRUDService[ShopReturnReason]):
    def __init__(self, repo: ShopReturnReasonSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> ShopReturnReasonSQLARepository:
        return self._repo

    def get_reasons(self, args: dict) -> Dict[str, Any]:
        """获取退货原因列表"""
        reason_type = args.get("reason_type")
        is_enabled = args.get("is_enabled")
        page = args.get("page")
        size = args.get("size")

        query_params = {"need_total_count": True}
        if page:
            query_params["page"] = page
        if size:
            query_params["size"] = size
        if reason_type:
            query_params["reason_type"] = reason_type
        if is_enabled is not None:
            query_params["is_enabled"] = is_enabled

        data, total = self._repo.list(**query_params)
        return dict(data=data, code=200, total=total)

    def get_enabled_reasons(self) -> Dict[str, Any]:
        """获取所有启用的退货原因"""
        data = self._repo.get_enabled_reasons()
        return dict(data=data, code=200)

    def get_by_id(self, reason_id: int) -> Dict[str, Any]:
        """获取指定ID的退货原因"""
        data = self._repo.get_by_id(reason_id)
        if not data:
            return dict(data=None, code=404, message="退货原因不存在")
        return dict(data=data, code=200)

    def create_reason(self, reason: ShopReturnReason) -> Dict[str, Any]:
        """创建退货原因"""
        current_user = get_current_user()
        if hasattr(current_user, 'username'):
            reason.updater = current_user.username

        # 验证数据
        if not reason.reason_type:
            return dict(data=None, code=400, message="原因类型不能为空")

        # 检查是否已存在相同类型
        existing = self._repo.find(reason_type=reason.reason_type)
        if existing:
            return dict(data=None, code=400, message="该退货原因类型已存在")

        result = self._repo.create(reason)
        return dict(data=result, code=200, message="退货原因创建成功")

    def update_reason(self, reason_id: int, reason: ShopReturnReason) -> Dict[str, Any]:
        """更新退货原因"""
        current_user = get_current_user()
        if hasattr(current_user, 'username'):
            reason.updater = current_user.username

        # 验证数据
        if not reason.reason_type:
            return dict(data=None, code=400, message="原因类型不能为空")

        # 检查是否存在
        existing = self._repo.get_by_id(reason_id)
        if not existing:
            return dict(data=None, code=404, message="退货原因不存在")

        # 检查是否与其他记录冲突
        conflict = self._repo.find(reason_type=reason.reason_type)
        if conflict and conflict.id != reason_id:
            return dict(data=None, code=400, message="该退货原因类型已存在")

        result = self._repo.update(reason_id, reason)
        return dict(data=result, code=200, message="退货原因更新成功")

    def delete_reason(self, reason_id: int) -> Dict[str, Any]:
        """删除退货原因"""
        existing = self._repo.get_by_id(reason_id)
        if not existing:
            return dict(code=404, message="退货原因不存在")

        self._repo.delete(reason_id)
        return dict(code=200, message="退货原因删除成功")

    def batch_delete(self, ids: List[int]) -> Dict[str, Any]:
        """批量删除退货原因"""
        if not ids:
            return dict(code=400, message="未提供要删除的ID列表")

        try:
            for reason_id in ids:
                self._repo.delete(reason_id, commit=False)

            self._repo.commit()
            return dict(code=200, message=f"成功删除了 {len(ids)} 个退货原因")
        except Exception as e:
            return dict(code=500, message=f"批量删除过程中发生错误: {str(e)}")

    def update_status(self, reason_id: int, is_enabled: bool) -> Dict[str, Any]:
        """更新退货原因状态"""
        current_user = get_current_user()

        existing = self._repo.get_by_id(reason_id)
        if not existing:
            return dict(data=None, code=404, message="退货原因不存在")

        # 设置更新人
        if hasattr(current_user, 'username'):
            existing.updater = current_user.username

        result = self._repo.update_status(reason_id, is_enabled)
        status_msg = "启用" if is_enabled else "禁用"
        return dict(data=result, code=200, message=f"退货原因已{status_msg}")

    def update_sort_order(self, reason_id: int, sort_order: int) -> Dict[str, Any]:
        """更新退货原因排序"""
        current_user = get_current_user()

        existing = self._repo.get_by_id(reason_id)
        if not existing:
            return dict(data=None, code=404, message="退货原因不存在")

        # 设置更新人
        if hasattr(current_user, 'username'):
            existing.updater = current_user.username

        result = self._repo.update_sort_order(reason_id, sort_order)
        return dict(data=result, code=200, message="退货原因排序已更新")
