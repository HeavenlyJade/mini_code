from typing import Optional, Dict, Any
from kit.service.base import CRUDService
from backend.mini_core.domain.card import Card

from backend.mini_core.repository.card.card_sqla import CardSQLARepository

__all__ = ['CardService']


class CardService(CRUDService[Card]):
    def __init__(self, repo: CardSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> CardSQLARepository:
        return self._repo

    def card_list(self, args: dict) -> Dict[str, Any]:
        """获取名片列表，支持分页和筛选"""
        # 添加需要统计总数的标记
        query_params = {"need_total_count": True}

        # 处理分页参数
        page = args.get("page")
        size = args.get("size")
        if page:
            query_params["page"] = page
        if size:
            query_params["size"] = size

        # 处理筛选条件
        if "name" in args and args["name"]:
            query_params["name"] = args["name"]
        if "company" in args and args["company"]:
            query_params["company"] = args["company"]
        if "position" in args and args["position"]:
            query_params["position"] = args["position"]
        if "phone" in args and args["phone"]:
            query_params["phone"] = args["phone"]
        if "weixing" in args and args["weixing"]:
            query_params["weixing"] = args["weixing"]

        data, total = self._repo.list(**query_params)
        return dict(data=data, code=200, total=total)

    def get(self, args: dict) -> Dict[str, Any]:
        """根据openid获取特定名片"""
        user_id = args.get("user_id")
        data = self._repo.find(user_id=user_id)
        if not data:
            return dict(data=None, code=404, message="未找到该名片")
        return dict(data=data, code=200)

    def update(self, card_id: int, card: Card) -> Dict[str, Any]:
        """更新名片信息"""
        # 检查名片是否存在
        existing = self._repo.find(**{"id":card_id})
        print("existing",existing)
        if not existing:
            return dict(data=None, code=404, message="未找到该名片")

        result = super().update(card_id, card)
        return dict(data=result, code=200, message="名片更新成功")

    def create(self, card: Card) -> Dict[str, Any]:
        """创建新名片"""
        # 检查是否已存在同一openid的名片
        if card.openid and self._repo.find(openid=card.openid):
            return dict(data=None, code=400, message="该openid已有名片，请使用更新接口")

        result = super().create(card)
        return dict(data=result, code=200, message="名片创建成功")

    def delete(self, card_id: int) -> Dict[str, Any]:
        """删除名片"""
        # 检查名片是否存在
        existing = self._repo.get_by_id(card_id)
        if not existing:
            return dict(data=None, code=404, message="未找到该名片")

        super().delete(card_id)
        return dict(code=200, message="名片删除成功")
