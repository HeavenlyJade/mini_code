from typing import Optional
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

    def get(self,args : dict) -> Optional[Card]:
        openid = args["openid"]
        data = self._repo.find(openid=openid)
        print(data)
        return dict(data=data,code=200)

    def update(self,openid:str,card:Card):
        return super().update(openid, card)

    def create(self,card:Card):
        return super().create(card)
    def delete(self,openid:str):
        return super().delete(openid)
