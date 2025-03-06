# -*- coding: utf-8 -*-
import json
import os

from backend.license_management.create_parsing_li.create_license import seperateKey, GetMacAddress
from backend.license_management.create_parsing_li.cryptoFunc import cy


_MONTH = ((0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31),
          (0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31))


def li_content(encryp_text):
    try:
        decryptText = cy.decrypt(encryp_text)
        pos = decryptText.find(seperateKey)
        if -1 == pos:
            # "解析 License 出错", ""
            return False
        cryptDataJson = cy.decrypt(decryptText[0:pos])
        crypt_data = json.loads(cryptDataJson)
        return crypt_data
    except Exception as e:
        return False

def get_date(d=0, m=0, y=0, start_date=None, format=""):
    if not start_date:
        import datetime
        start_date = datetime.datetime.now()
    if d != 0:
        start_date += datetime.timedelta(days=d)
    if not (y or m):
        if format == "date":
            return start_date.strftime("%Y-%m-%d")
        elif format == "date_time":
            return start_date.strftime("%m月%d日")
        return start_date.strftime("%Y-%m-%d %H:%M:%S")

    n = int(start_date.year) * 12 + int(start_date.month) - 1
    n = n + m
    ryear = n / 12
    rmonth = n % 12 + 1
    rday = start_date.day
    import calendar
    if calendar.isleap(ryear):
        if rday > _MONTH[1][rmonth]:
            rday = _MONTH[1][rmonth]
    else:
        if rday > _MONTH[0][rmonth]:
            rday = _MONTH[0][rmonth]

    y += (m + int(start_date.month) - 1) / 12
    result = start_date.replace(year=start_date.year + y, month=rmonth, day=rday)
    if format == "date":
        return result.strftime("%Y-%m-%d")
    elif format == "date_time":
        return start_date.strftime("%m月%d日")
    return result.strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    # filePath = r"D:\work\workSpace\backend-backend\backend\license_management\create_parsing_li\license.lic"
    # try:
    #     ok, msg, expireTime = getLicenseInfo(filePath)
    # except:
    #     sys.exit()
    # print(ok, msg, expireTime)
    data = '79b2a0f046e32157e7d765b5db50d77a9a8c2536520da718d253d21b089da02feb2c066d93b84017fa11a5067a396333fca3346824f5577ba75b4e72ccfe87c8271c08e172d4282138a2bdc5a4afe8b3db50f928846c0a5e7d85282868b2cf65d851ad46daeff7cd0bace6b425c8ac991c23e2e11b4e47fb0645c1603be37903946a252912573d81b1a36143ed56fb78efaeb870a586258fb27c1e13df9cddd6354bca4d6148053983e7c4ba24553781d54f5ec46a1b7c07a52aa89bce657df4af201963a33f32a9005039925818b1133daf233ee622123f7db3de62dbf63e2eefa0f6c3f16322d8bc82fbd32ca39e6a5a083f18e749744cb479898af88c093043641889413477f9f8e4843f7b157c82eab8efd5f192f40411785c066e7e66d9ae7663308a83dc28abe6c724753a0e7d'
    print(li_content(data))
