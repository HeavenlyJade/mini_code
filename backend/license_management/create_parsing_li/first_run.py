# -*- coding: utf-8 -*-
# author zyy
import argparse
import json
import os.path
import platform
import socket
import sys
from binascii import b2a_hex

import netifaces
from Crypto.Cipher import AES
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()



seperateKey = "d#~0^38J:"  # 随意输入一组字符串
aesKey = "123456789abcdefg"  # 加密与解密所使用的密钥，长度必须是16的倍数
aesIv = "abcdefg123456789"  # initial Vector,长度要与aesKey一致
aesModel = AES.MODE_CBC


# 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
def encrypt(text):
    cryptor = AES.new(aesKey.encode("utf8"), aesModel, aesIv.encode("utf8"))
    # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
    length = 16
    count = len(text)
    if (count % length != 0):
        add = length - (count % length)
    else:
        add = 0
    text = text + ('\0' * add)
    text = text.encode("utf8")
    ciphertext = cryptor.encrypt(text)
    # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
    # 所以这里统一把加密后的字符串转化为16进制字符串
    return b2a_hex(ciphertext).decode('utf-8')


class GetMacAddress(object):
    def __init__(self):
        self.ip = ''
        self.__mac = ''

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('114.114.114.114', 80))
            self.ip = s.getsockname()[0]
        finally:
            s.close()

    def get_mac_address(self):
        # 根据指定的ip地址获取mac：00:50:56:c0:00:08
        for i in netifaces.interfaces():
            addrs = netifaces.ifaddresses(i)
            try:
                if_mac = addrs[netifaces.AF_LINK][0]['addr']
                if_ip = addrs[netifaces.AF_INET][0]['addr']
                if if_ip == self.ip:
                    self.__mac = if_mac
                    break
            except KeyError as e:
                pass

    def mac(self):
        if platform.system().lower() == 'linux':
            with open('/sys/class/dmi/id/product_uuid', 'r') as f:
                self.__mac = f.read().strip("\n")
        else:
            self.get_ip_address()
            self.get_mac_address()
        return self.__mac


class LicenseManagement(Base):
    __tablename__ = 'license_management'
    id = Column(Integer, primary_key=True)
    customer_name = Column(String(50))
    unique_code = Column(String(50))
    license = Column(String(2000))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    is_del = Column(Integer)


class FirstRun:
    def __init__(self, db_info):
        self.engine = create_engine(db_info, echo=True)
        # 创建会话
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def insert_li(self, data):
        # 将字典转换成ORM对象
        try:
            li_info = LicenseManagement(**data)
            # 将ORM对象添加到会话中并提交
            self.session.add(li_info)
            self.session.commit()
        finally:
            self.session.close()

    def create_license(self, data):
        text = json.dumps(text_data)
        encryptText = encrypt(text)
        encryptText = encryptText + seperateKey + "Valid"
        encryptText = encrypt(encryptText)
        data['license'] = encryptText
        data['is_del'] = 0
        self.insert_li(data)
        print("证书配置: %s" % text_data)


if __name__ == '__main__':
    db_info = 'mysql+pymysql://root:root@192.168.10.159:3306/backend?charset=utf8mb4'
    unique_code = GetMacAddress().mac()
    # 唯一标识在此添加是吗
    text_data = {}
    text_data['customer_name'] = '晶合'
    text_data['unique_code'] = unique_code
    text_data['start_time'] = '2013-04-12 17:43:05'
    text_data['end_time'] = '2025-07-1 17:43:06'
    obj_fri = FirstRun(db_info)
    obj_fri.create_license(text_data)

