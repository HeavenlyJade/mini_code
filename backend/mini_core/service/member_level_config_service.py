import json
from typing import Dict, Any, List, Optional
from decimal import Decimal
from flask_jwt_extended import get_current_user

from kit.service.base import CRUDService
from backend.mini_core.domain.member_level import MemberLevelConfig
from backend.mini_core.repository.shop.member_level_config import MemberLevelConfigSQLARepository

__all__ = ['MemberLevelConfigService']


class MemberLevelConfigService(CRUDService[MemberLevelConfig]):
    def __init__(self, repo: MemberLevelConfigSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> MemberLevelConfigSQLARepository:
        return self._repo

    def get_level_list(self, args: dict) -> Dict[str, Any]:
        """
        获取会员等级列表

        Args:
            args: 查询参数，可包含以下内容:
                - level_code: 等级代码
                - level_name: 等级名称
                - upgrade_condition_type: 升级条件类型
                - is_enabled: 是否启用
                - page: 页码
                - size: 每页条数

        Returns:
            Dict: 包含等级列表和总数的字典
        """
        # 设置默认排序
        if 'ordering' not in args:
            args['ordering'] = ['-level_value']
        data, total = self._repo.list(**args)
        return dict(data=data, total=total, code=200)

    def get_enabled_levels(self) -> Dict[str, Any]:
        """
        获取所有启用的会员等级

        Returns:
            Dict: 包含启用等级列表的字典
        """
        data = self._repo.get_enabled_levels()
        return dict(data=data, code=200, total=len(data))

    def find_level_data(self,args):
        return self._repo.find(**args)
    def get_level_by_id(self, level_id: int) -> Dict[str, Any]:
        """
        根据ID获取等级配置

        Args:
            level_id: 等级ID

        Returns:
            Dict: 包含等级配置的字典
        """
        data = self._repo.get_by_id(level_id)
        if not data:
            return dict(data=None, code=404, message="等级配置不存在")
        return dict(data=data, code=200)

    def create_level(self, level_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建会员等级配置

        Args:
            level_data: 等级配置数据

        Returns:
            Dict: 包含创建结果的字典
        """
        # 验证必要字段
        required_fields = ['level_code', 'level_name', 'level_value']
        for field in required_fields:
            if field not in level_data or not level_data[field]:
                return dict(data=None, code=400, message=f"缺少必要字段: {field}")

        # 检查等级代码是否已存在
        if self._repo.check_level_code_exists(level_data['level_code']):
            return dict(data=None, code=400, message="等级代码已存在")

        # 检查等级数值是否已存在
        existing_level = self._repo.get_by_level_value(level_data['level_value'])
        if existing_level:
            return dict(data=None, code=400, message="等级数值已存在")

        # 设置创建者
        current_user = get_current_user()
        if hasattr(current_user, 'username'):
            level_data['creator'] = current_user.username

        # 处理 benefits 字段（如果是字典，转换为JSON字符串）
        if 'benefits' in level_data and isinstance(level_data['benefits'], dict):
            level_data['benefits'] = json.dumps(level_data['benefits'])

        level = MemberLevelConfig(**level_data)
        result = self._repo.create(level)
        return dict(data=result, code=200, message="等级配置创建成功")

    def update_level(self, level_id: int, level_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新会员等级配置

        Args:
            level_id: 等级ID
            level_data: 更新的等级数据

        Returns:
            Dict: 包含更新结果的字典
        """
        # 检查是否存在
        existing = self._repo.get_by_id(level_id)
        if not existing:
            return dict(data=None, code=404, message="等级配置不存在")

        # 如果修改了等级代码，检查是否冲突
        if 'level_code' in level_data and level_data['level_code'] != existing.level_code:
            if self._repo.check_level_code_exists(level_data['level_code'], level_id):
                return dict(data=None, code=400, message="等级代码已存在")

        # 如果修改了等级数值，检查是否冲突
        if 'level_value' in level_data and level_data['level_value'] != existing.level_value:
            conflict_level = self._repo.get_by_level_value(level_data['level_value'])
            if conflict_level and conflict_level.id != level_id:
                return dict(data=None, code=400, message="等级数值已存在")

        # 设置更新者
        current_user = get_current_user()
        if hasattr(current_user, 'username'):
            level_data['updater'] = current_user.username

        # 处理 benefits 字段
        if 'benefits' in level_data and isinstance(level_data['benefits'], dict):
            level_data['benefits'] = json.dumps(level_data['benefits'])

        level = MemberLevelConfig(**level_data)
        result = self._repo.update(level_id, level)
        return dict(data=result, code=200, message="等级配置更新成功")

    def delete_level(self, level_id: int) -> Dict[str, Any]:
        """
        删除会员等级配置

        Args:
            level_id: 等级ID

        Returns:
            Dict: 包含删除结果的字典
        """
        existing = self._repo.get_by_id(level_id)
        if not existing:
            return dict(data=None, code=404, message="等级配置不存在")

        # TODO: 检查是否有用户正在使用此等级
        # 这里可以添加业务逻辑检查

        self._repo.delete(level_id)
        return dict(code=200, message="等级配置删除成功")


