data = {'data': {'amount': {'currency': 'CNY', 'payer_currency': 'CNY', 'payer_total': 1, 'total': 1},
                 'appid': 'wx755aabf27ec3641d', 'attach': '', 'bank_type': 'OTHERS', 'mchid': '1713205797',
                 'out_trade_no': 'ORD20250515150138228897', 'payer': {'openid': 'od-Km7eh_iuz-f8qUhjQ2OfJtGwM'},
                 'promotion_detail': [], 'success_time': '2025-05-16T13:48:59+08:00', 'trade_state': 'SUCCESS',
                 'trade_state_desc': '支付成功', 'trade_type': 'JSAPI',
                 'transaction_id': '4200002679202505165863584296'}, 'code': 200}
data = data.get("data")
print(data)
transaction_id = data.get('transaction_id')
trade_state_desc = data.get('trade_state_desc')
print(trade_state_desc)
print(transaction_id)
