import json
import time
import uuid
import base64
import os
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
appid = "wxd678efh567hg6787"
mchid = "1900007291"
description = "Image形象店-深圳腾大-QQ公仔"
out_trade_no = "1217752501201407033233368018"
notify_url = "https://www.weixin.qq.com/wxpay/pay.php"
amount = {"total":100,"currency":"CNY"}
payer = {"openid":"oUpF8uMuAJO_M2pxb1Q9zNjWeS6o"}
method="POST"
url_parts="/v3/pay/transactions/jsapi"
timestamp="1554208460"
nonce_str="593BEC0C930BF1AFEB40B4A08C8FB242"
body={"appid":"wxd678efh567hg6787","mchid":"1900007291","description":"Image形象店-深圳腾大-QQ公仔","out_trade_no":"1217752501201407033233368018","notify_url":"https://www.weixin.qq.com/wxpay/pay.php","amount":{"total":100,"currency":"CNY"},"payer":{"openid":"oUpF8uMuAJO_M2pxb1Q9zNjWeS6o"}}
body=json.dumps(body)
private_key_str ="""-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAptpm+qvIDCh/9wjU26SQCK26ogYkBhDrYxnAaw2JbbBsp1oD
bHKk+1r381NeBUG2HEFAuU+Fr72u5ot3yKdzoF/FajAzQNKnm569/D3upKoi8mYB
aST15Uig8j8qoUW1U217LL0jEHlSnHV3lcaDTXqDpTRR4Bfz9IqOgJgFZ8/oTfEo
mSrjrLYef81Eyxr7ZIMQXEKKEK7V4UXKS0+/fDsiG/cXidhzt8UbTL9vqXqxM2+I
DImyO+FAc/tkBG55LmzxPto1Nq0WbnZzRM/wTzrd0I/8NlevxtFbphg4evlHjFNI
7+GrqR87ViEwuAJJ9Je5QQjct5YJfFRWiZ5CMQIDAQABAoIBAGBi/GhEgezcHIg1
ltlHaFlLGuxsRbUnYwM9phVxnXk7GJlYe2/TjpERjPkIqOC6hBwwadZjJORP3FCc
Mtc8PKRhjuZ377O7vU0915x2nnyLOGL1IE2AJ3iLi0ZFzTea0FPgg+5lWHM00s9F
YI6qPcGtS41M+xtMWwZiYE3TBBRibHiY8ugGyaNAhiMKehyW05uApjlIF55wwCGx
BkyESJpGRR/6853iHke6Ge+xVcMa9QmQdoH0QqL/8kT28PL568mJJr0Ow/83t4+d
Pe70YPzKAxgUnaDsHJqO+b8qH69AEs8rTI5h2Mon6pH+bJT66KUoiXhn+Kf+4LSs
henRP10CgYEA1QJSfuFOWVRjrg3N/rAIc/Ak84BTZavbyrkqBSuoTs9i/nMI/hOz
VxpDntg7Bx2Tctl6sZO3GioTxKdc/YYaTKci1TKBbeginpsqEQVgwkMCy8HpvUmR
fyAMqLwZC4h9+j+NiZtuoFJDTCgv+WYbasX+kWYEUM21bnSYuO7yEQsCgYEAyIdP
r9uzqPgzN34Tmx+CNTa16VjhBh+zkBtXRLDLhWBeIYxoYNJARD98Pb1XZdvpkZZW
Sk7MfaKo2/DomzyyyB/MbHWwAdFi3yb4y7uMJfyC1MzdUSNN3Vp579hJxHkJ+nN4
Ys76yfcEeVOLnvUT1Z0KKCdIWRdT1Lgi+X1itzMCgYBJUXlPzwGG4fNFj97d0X23
Wmt9nSgXkOYgi0eZbAOMzPmIF9R6kBFk49dur4Lx2g5Ms+r1gKC/0sfnIqxxX11i
EQ1+UNoYGJUB/uql3TIG68XkmKR50P7RwRhaZBRC0gJ6xrFTMjsL2ATuC88niyvY
vrn3FiRaI9RVZrDCxwxvLQKBgEXW4okEAqGBuAzGqztmkOnJoTehDdYdKmOxMgap
cGiGdKJIjX3THDDoz3ONQyglnEZpTqpYoV3MTfU0BT8zt6x9bqwDnQY1D7NalmIW
cqw0Mri8lQQSQKcsQLWo5aA466G/n5kCL1Qx5OwAjesRvhOyuvvbGpZ0ymyWqQ+t
fLkDAoGATcul1L8y5D/wNVP1GXbXMZfBsFP3bbqy8c+Ashm6g8OLm2mGNntd5Z6h
1KkID7Yksh+dZ6t7XaPBtGACXX5Eryr537JVvdX8hAVCp5HVtaN/9VBVP8Ka2e4s
VS/xeNgOMQ7uzhRPBJ8HiTmdI1nHhDnYQpGiBgQn0Z5RAkSvFMk=
-----END RSA PRIVATE KEY-----"""
# 使用私钥对签名串进行签名
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_der_private_key
private_key_path = "D:/code/git/mini_code/wxcert/text.pem"

# 读取私钥文件内容
with open(private_key_path, 'rb') as f:
    private_key = load_pem_private_key(
        f.read(),
        password=None,
        backend=default_backend()
    )

message = """POST\n
/v3/pay/transactions/jsapi\n
1554208460\n
593BEC0C930BF1AFEB40B4A08C8FB242\n
{"appid":"wxd678efh567hg6787","mchid":"1900007291","description":"Image形象店-深圳腾大-QQ公仔","out_trade_no":"1217752501201407033233368018","notify_url":"https://www.weixin.qq.com/wxpay/pay.php","amount":{"total":100,"currency":"CNY"},"payer":{"openid":"oUpF8uMuAJO_M2pxb1Q9zNjWeS6o"}}\n"""

signature_bytes = private_key.sign(
    message.encode('utf-8'),
    PKCS1v15(),
    SHA256()
)
signature = base64.b64encode(signature_bytes).decode('utf-8')
print(signature)
