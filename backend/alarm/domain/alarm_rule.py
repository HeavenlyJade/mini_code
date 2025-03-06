from dataclasses import dataclass, field

from kit.domain.entity import Entity

__all__ = ['AlarmRule']


@dataclass
class AlarmRule(Entity):
    recipe_upper_limit: float = field(
        default=None, metadata=dict(required=True, description='recipe 范围上限值')
    )

    recipe_lower_limit: float = field(
        default=None, metadata=dict(required=True, description='recipe 范围上限值')
    )
