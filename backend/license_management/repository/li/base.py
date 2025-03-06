# -*- coding: utf-8 -*-
# author zyy
from abc import ABCMeta

from backend.business.domain.product import Product
from backend.license_management.domain.li import License
from kit.repository.generic import GenericRepository

__all__ = ['LiRepository']


class LiRepository(GenericRepository[License], metaclass=ABCMeta):
    ...
