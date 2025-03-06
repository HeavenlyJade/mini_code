# -*- coding: utf-8 -*-
# author zyy
from backend.license_management.create_parsing_li.create_license import GetMacAddress
from backend.license_management.create_parsing_li.get_license import li_content, get_date
from backend.license_management.domain.li import License

from kit.service.base import CRUDService

__all__ = ['LiService']


class LiService(CRUDService[License]):

    def query_by_time(self, args: dict):
        data = self.repo.find_time(args)
        return data

    def del_li_id(self, id: int):
        data = self.repo.delete_li(id)
        return data

    def is_legal(self, content) -> bool:
        li_info = li_content(str(content))
        mac = GetMacAddress().mac()
        if li_info and 'end_time' in li_info.keys() \
            and 'start_time' in li_info.keys() \
            and 'customer_name' in li_info.keys() \
            and 'unique_code' in li_info.keys():

            if get_date() <= li_info["end_time"] and li_info["unique_code"] == mac:
                # 同一个li进制同时插入 未删除
                if not self.repo.is_exist(str(content)):
                    li_info['license'] = str(content)
                    self.create(li_info)
                    return True
        return False
