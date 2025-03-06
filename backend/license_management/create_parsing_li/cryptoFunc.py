# -*- coding: utf-8 -*-
import random
import string
from binascii import b2a_hex, a2b_hex

from Crypto.Cipher import AES

seperateKey = "d#~0^38J:"       # 随意输入一组字符串
aesKey = "123456789abcdefg"     # 加密与解密所使用的密钥，长度必须是16的倍数
aesIv = "abcdefg123456789"      # initial Vector,长度要与aesKey一致
aesMode = AES.MODE_CBC          # 使用CBC模式


# 生成AES密匙
def random_password(num):
    result = ''
    choice = '0123456789' + string.ascii_lowercase
    result += random.choice('0123456789')
    result += random.choice(string.ascii_lowercase)
    list = []
    for i in range(num - 2):
        a = random.choice(choice)
        list.append(a)
        result += a
    return result


class TCrypt():
    def __init__(self, key, aesIv):
        self.key = key.encode("utf8")
        self.mode = AES.MODE_CBC
        self.iv = aesIv.encode("utf8")

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)
        if (count % length != 0):
            add = length - (count % length)
        else:
            add = 0
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext).decode('utf-8')

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        plain_text = cryptor.decrypt(a2b_hex(text))
        plain_text = plain_text.decode('ascii')
        return plain_text.rstrip('\0')


cy = TCrypt(aesKey, aesIv)

