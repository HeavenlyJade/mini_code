from typing import Optional, List, Dict, Any
from kit.service.base import CRUDService
from backend.mini_core.domain.specification import ShopSpecification, ShopSpecificationAttribute
from backend.mini_core.repository.shop.shop_specification import ShopSpecificationSQLARepository, \
    ShopSpecificationAttributeSQLARepository

__all__ = ['ShopSpecificationService', 'ShopSpecificationAttributeService']


class ShopSpecificationService(CRUDService[ShopSpecification]):
    def __init__(self, repo: ShopSpecificationSQLARepository, attr_repo: ShopSpecificationAttributeSQLARepository):
        super().__init__(repo)
        self._repo = repo
        self._attr_repo = attr_repo

    @property
    def repo(self) -> ShopSpecificationSQLARepository:
        return self._repo

    def get_list(self, args: dict) -> Dict[str, Any]:
        """根据条件获取规格列表"""
        specification_id = args.get("id")
        if specification_id:
            data = self._repo.get(specification_id)
            return dict(data=data, code=200)
        # 支持按名称查询
        name = args.get("name")
        page = args.get("page")
        size = args.get("size")
        query_params = {"need_total_count": True}
        if page:
            query_params["page"] = page
        if size:
            query_params["size"] = size
        if name:
            query_params['name'] = name

        data, total = self._repo.list(**query_params)
        return dict(data=data, code=200, total=total)

    def get_by_id(self, specification_id: int) -> Dict[str, Any]:
        """获取指定ID的规格"""
        data = self._repo.get_by_id(specification_id)
        return dict(data=data, code=200)

    def get_with_attributes(self, specification_id: int) -> Dict[str, Any]:
        """获取规格及其属性"""
        specification = self._repo.get_by_id(specification_id)
        if not specification:
            return dict(data=None, code=404, message="规格不存在")

        attributes = self._attr_repo.get_attributes_by_specification(specification_id)
        result = {
            "specification": specification,
            "attributes": attributes
        }
        return dict(data=result, code=200)

    def create_specification(self, specification: ShopSpecification) -> Dict[str, Any]:
        """创建规格"""
        result = super().create(specification)
        return dict(data=result, code=200)

    def update_specification(self, specification_id: int, specification: ShopSpecification) -> Dict[str, Any]:
        """更新规格"""
        result = super().update(specification_id, specification)
        return dict(data=result, code=200)

    def delete_specification(self, specification_id: int) -> Dict[str, Any]:
        """删除规格及其属性"""
        # 先删除关联的属性
        attributes = self._attr_repo.get_attributes_by_specification(specification_id)
        for attr in attributes:
            self._attr_repo.delete(attr.id)

        # 再删除规格
        super().delete(specification_id)
        return dict(data=None, code=200, message="删除成功")

    def batch_delete(self, ids: List[int]) -> Dict[str, Any]:
        """批量删除规格"""
        if not ids:
            return dict(data=None, code=400, message="未提供要删除的规格ID")

        # 预检查所有规格
        for specification_id in ids:
            # 删除关联的属性
            attributes = self._attr_repo.get_attributes_by_specification(specification_id)
            for attr in attributes:
                self._attr_repo.delete(attr.id, commit=False)

            # 删除规格
            self._repo.delete(specification_id, commit=False)

        # 提交事务
        self._repo.commit()
        return dict(data={"deleted_ids": ids}, code=200, message=f"成功删除了 {len(ids)} 个规格")


class ShopSpecificationAttributeService(CRUDService[ShopSpecificationAttribute]):
    def __init__(self, repo: ShopSpecificationAttributeSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> ShopSpecificationAttributeSQLARepository:
        return self._repo

    def get_list(self, args: dict) -> Dict[str, Any]:
        """根据条件获取规格属性列表"""
        attribute_id = args.get("id")
        if attribute_id:
            data = self._repo.get(attribute_id)
            return dict(data=data, code=200)

        # 支持按规格ID查询
        specification_id = args.get("specification_id")
        name = args.get("name")
        page = args.get("page")
        size = args.get("size")
        query_params = {"need_total_count": True}
        if page:
            query_params["page"] = page
        if size:
            query_params["size"] = size
        if specification_id:
            query_params['specification_id'] = specification_id
        if name:
            query_params['name'] = name

        data, total = self._repo.list(**query_params)
        return dict(data=data, code=200, total=total)

    def get_by_id(self, attribute_id: int) -> Dict[str, Any]:
        """获取指定ID的规格属性"""
        data = self._repo.get_by_id(attribute_id)
        return dict(data=data, code=200)

    def get_by_specification(self, specification_id: int) -> Dict[str, Any]:
        """获取指定规格ID的所有属性"""
        data = self._repo.get_attributes_by_specification(specification_id)
        return dict(data=data, code=200)

    def create_attribute(self, attribute: ShopSpecificationAttribute) -> Dict[str, Any]:
        """创建规格属性"""
        result = super().create(attribute)
        return dict(data=result, code=200)

    def update_attribute(self, attribute_id: int, attribute: ShopSpecificationAttribute) -> Dict[str, Any]:
        """更新规格属性"""
        result = self._repo.update_attribute(attribute_id, attribute)
        return dict(data=result, code=200)

    def delete_attribute(self, attribute_id: int) -> Dict[str, Any]:
        """删除规格属性"""
        super().delete(attribute_id)
        return dict(data=None, code=200, message="删除成功")

    def batch_delete(self, ids: List[int]) -> Dict[str, Any]:
        """批量删除规格属性"""
        if not ids:
            return dict(data=None, code=400, message="未提供要删除的属性ID")

        # 批量删除
        for attribute_id in ids:
            self._repo.delete(attribute_id, commit=False)

        # 提交事务
        self._repo.commit()
        return dict(data={"deleted_ids": ids}, code=200, message=f"成功删除了 {len(ids)} 个属性")
