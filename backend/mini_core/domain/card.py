from dataclasses import field

from marshmallow_dataclass import dataclass

from kit.domain.entity import Entity

@dataclass
class CardQuery(Entity):
    openid: str = field(
        default=None,
        metadata=dict(
            description='微信的openid',
        ),
    )
@dataclass
class Card(Entity):
    name: str = field(
        default=None,
        metadata=dict(
            description='用户名称',
        ),
    )
    openid: str = field(
        default=None,
        metadata=dict(
            description='微信的openid',
        ),
    )
    position: str = field(
        default=None,
        metadata=dict(
            description='职位',
        ),
    )
    company: str = field(
        default=None,
        metadata=dict(
            description='公司',
        ),
    )
    phone: str = field(
        default=None,
        metadata=dict(
            description='电话',
        ),
    )
    weixing: str = field(
        default=None,
        metadata=dict(
            description='微信',
        ),
    )



