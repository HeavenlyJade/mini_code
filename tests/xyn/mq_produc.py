import json

RPT_OV_MEASUREDATA = {
    "msgHead": {"traceId": "backendCS#20231228142726118", "rqstId": "20231228142726118", "srvName": "backend", "srvEnv": "Prod",
                "rqstAddr": None, "srvAddr": None, "service": "backendCS", "msgType": "R", "locale": None, "txId": 1,
                "rqstTime": "20231228142726118", "retCode": 0, "retMsg": ""},
    "msgBody": {"CMD": "RPT_OV_MEASUREDATA", "AREA": "PHOTO", "BATCHID": "20231228142726118", "EQPID": "AMOL01",
                "RequestDatas": [{"PITCHSIZE": "24.42972 32.39196", "EDCSPECLIST": [{"EDCSPECNAME": "OVL-RAWDATA",
                                                                                     "WAFER_DATA": [
                                                                                         {"WAFERID": "AL0001#01",
                                                                                          "SLOTID": 1,
                                                                                          "COLLECTEDDATA": [{
                                                                                                                "RELATIVE_COORDINATE": "0 0",
                                                                                                                "SITEID": 1,
                                                                                                                "RAWDATA": "-0.0378 0.039"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "3 1",
                                                                                                                "SITEID": 1,
                                                                                                                "RAWDATA": "-0.0301 0.03555"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "0 -3",
                                                                                                                "SITEID": 1,
                                                                                                                "RAWDATA": "0.03955 -0.00185"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "0 3",
                                                                                                                "SITEID": 1,
                                                                                                                "RAWDATA": "-0.051 -0.01685"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "-5 0",
                                                                                                                "SITEID": 1,
                                                                                                                "RAWDATA": "0.02895 0.02715"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "-3 2",
                                                                                                                "SITEID": 1,
                                                                                                                "RAWDATA": "-0.05925 0.05585"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "-2 0",
                                                                                                                "SITEID": 1,
                                                                                                                "RAWDATA": "-0.02655 -0.0233"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "3 -1",
                                                                                                                "SITEID": 1,
                                                                                                                "RAWDATA": "0.0096 0.05935"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "-3 -2",
                                                                                                                "SITEID": 1,
                                                                                                                "RAWDATA": "-0.01935 0.01995"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "0 0",
                                                                                                                "SITEID": 2,
                                                                                                                "RAWDATA": "-0.0237 0.0376"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "3 1",
                                                                                                                "SITEID": 2,
                                                                                                                "RAWDATA": "-0.044 0.02555"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "0 -3",
                                                                                                                "SITEID": 2,
                                                                                                                "RAWDATA": "-0.01175 0.02545"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "0 3",
                                                                                                                "SITEID": 2,
                                                                                                                "RAWDATA": "-0.0833 -0.01925"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "-5 0",
                                                                                                                "SITEID": 2,
                                                                                                                "RAWDATA": "-0.02885 0.02475"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "-3 2",
                                                                                                                "SITEID": 2,
                                                                                                                "RAWDATA": "-0.08175 0.04245"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "-2 0",
                                                                                                                "SITEID": 2,
                                                                                                                "RAWDATA": "-0.08915 0.0052"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "3 -1",
                                                                                                                "SITEID": 2,
                                                                                                                "RAWDATA": "-0.048 0.03945"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "-3 -2",
                                                                                                                "SITEID": 2,
                                                                                                                "RAWDATA": "-0.01935 -0.02795"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "0 0",
                                                                                                                "SITEID": 3,
                                                                                                                "RAWDATA": "0.0079 -0.007"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "3 1",
                                                                                                                "SITEID": 3,
                                                                                                                "RAWDATA": "-0.0313 0.05175"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "0 -3",
                                                                                                                "SITEID": 3,
                                                                                                                "RAWDATA": "0.01905 0.00855"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "0 3",
                                                                                                                "SITEID": 3,
                                                                                                                "RAWDATA": "-0.0804 0.03665"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "-5 0",
                                                                                                                "SITEID": 3,
                                                                                                                "RAWDATA": "0.01405 0.05825"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "-3 2",
                                                                                                                "SITEID": 3,
                                                                                                                "RAWDATA": "-0.05375 0.03595"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "-2 0",
                                                                                                                "SITEID": 3,
                                                                                                                "RAWDATA": "-0.00545 -0.0026"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "3 -1",
                                                                                                                "SITEID": 3,
                                                                                                                "RAWDATA": "0.0095 0.03465"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "-3 -2",
                                                                                                                "SITEID": 3,
                                                                                                                "RAWDATA": "0.00515 -0.00685"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "0 0",
                                                                                                                "SITEID": 4,
                                                                                                                "RAWDATA": "0.0002 0.0184"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "3 1",
                                                                                                                "SITEID": 4,
                                                                                                                "RAWDATA": "-0.0006 0.07295"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "0 -3",
                                                                                                                "SITEID": 4,
                                                                                                                "RAWDATA": "0.05595 0.03635"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "0 3",
                                                                                                                "SITEID": 4,
                                                                                                                "RAWDATA": "-0.0375 0.00935"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "-5 0",
                                                                                                                "SITEID": 4,
                                                                                                                "RAWDATA": "0.07905 0.09355"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "-3 2",
                                                                                                                "SITEID": 4,
                                                                                                                "RAWDATA": "-0.03885 0.04105"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "-2 0",
                                                                                                                "SITEID": 4,
                                                                                                                "RAWDATA": "0.01425 0.0061"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "3 -1",
                                                                                                                "SITEID": 4,
                                                                                                                "RAWDATA": "0.0618 0.03585"},
                                                                                                            {
                                                                                                                "RELATIVE_COORDINATE": "-3 -2",
                                                                                                                "SITEID": 4,
                                                                                                                "RAWDATA": "-0.00205 0.00885"}]}]}],
                                  "LOT_ID": "AL0001", "CARRIERID": "C000001", "PRODUCTID": "V08856-A01P",
                                  "STAGENAME": "PP", "STEPID": "XX", "RUNCARDFLAG": 0}], "ResponseDatas": None}}

RPT_CD_MEASUREDATA = {
    "msgHead": {"traceId": "backendCS#20231228141309885", "rqstId": "20231228141309885", "srvName": "backend", "srvEnv": "Prod",
                "rqstAddr": None, "srvAddr": None, "service": "backendCS", "msgType": "R", "locale": None, "txId": 1,
                "rqstTime": "20231228141309885", "retCode": 0, "retMsg": ""},
    "msgBody": {"CMD": "RPT_CD_MEASUREDATA", "AREA": "PHOTO", "BATCHID": "20231228141309885", "EQPID": "AMCD01",
                "RequestDatas": [{"EDCSPECLIST": [{"EDCSPECNAME": "AL-M0001FBA-PLUPH-CD1", "WAFER_DATA": [
                    {"WAFERID": "AL0001#01", "SLOTID": 1,
                     "RAWDATA": ["0.0856001", "0.0821745545", "0.0870155543", "0.08969937", "0.08595101", "0.07903963",
                                 "0.08615057", "0.08696825", "0.08838703"]}]}], "LOT_ID": "AL0001",
                                  "CARRIERID": "CPFE00024", "PRODUCTID": "-A01P", "STAGENAME": "PP",
                                  "STEPID": "PP1CD1", "RUNCARDFLAG": 0}], "ResponseDatas": None}}

RPT_EXP_PROCESSSTART = {
    "msgHead": {"traceId": "backendCS#20231228100532564", "rqstId": "20231228100532564", "srvName": "backend", "srvEnv": "Prod",
                "rqstAddr": None, "srvAddr": None, "service": "backendCS", "msgType": "R", "locale": None, "txId": 1,
                "rqstTime": "20231228100532564", "retCode": 0, "retMsg": ""},
    "msgBody": {"CMD": "RPT_EXP_PROCESSSTART", "AREA": "PHOTO", "BATCHID": "20231228100532564", "EQPID": "ALST01",
                "RequestDatas": [{"EXPOSURE_RECIPE": "Flatness@TTT", "MASK": "M000101APLU1",
                                  "WAFERS": ["AP00005#04", "AP00005#03", "AP00005#02"], "LOT_ID": "AP00005",
                                  "CARRIERID": "CPFE00005", "PRODUCTID": "0726P", "STAGENAME": "BP-DEP1",
                                  "STEPID": "BIFURINS2", "RUNCARDFLAG": 0},
                                 {"EXPOSURE_RECIPE": "Flatnes1@TT1", "MASK": "M000101APLU1", "WAFERS": ["AP00005#01"],
                                  "LOT_ID": "AP00005.01", "CARRIERID": "CPFE00005", "PRODUCTID": "0726P",
                                  "STAGENAME": "BP-DEP1", "STEPID": "BIFURINS2", "RUNCARDFLAG": 0}],
                "ResponseDatas": None}}
RPT_EXP_PROCESSEND = {
    "msgHead": {"traceId": "backendCS#20231228102934075", "rqstId": "20231228102934075", "srvName": "backend", "srvEnv": "Prod",
                "rqstAddr": None, "srvAddr": None, "service": "backendCS", "msgType": "R", "locale": None, "txId": 1,
                "rqstTime": "20231228102934075", "retCode": 0, "retMsg": ""},
    "msgBody": {"CMD": "RPT_EXP_PROCESSEND", "AREA": "PHOTO", "BATCHID": "20231228102934075", "EQPID": "ALST01",
                "RequestDatas": [{"EXPOSURE_RECIPE": "Flatness@TTT", "MASK": "M000101APLU1",
                                  "WAFERS": ["AP00005#04", "AP00005#03", "AP00005#02"], "ENERGY": "0000000.00",
                                  "FOCUS": "0000000.00", "OFFSETX": "0000000.00", "OFFSETY": "0000000.00",
                                  "SCALINGX": "0000000.00", "SCALINGY": "0000000.00", "WFR_ROT": "0000000.00",
                                  "ORTHO": "0000000.00", "RET_SCALING": "0.083", "RET_ROT": "0.458", "EXP_MODE": None,
                                  "ENERGY_STEP": None, "FOCUS_STEP": None, "PROCESSINFO": None, "LOT_ID": "AP00005",
                                  "CARRIERID": "CPFE00005", "PRODUCTID": "0726P", "STAGENAME": "BP-DEP1",
                                  "STEPID": "BIFURINS2", "RUNCARDFLAG": 0},
                                 {"EXPOSURE_RECIPE": "Flatnes1@TT1", "MASK": "M000101APLU1", "WAFERS": ["AP00005#01"],
                                  "ENERGY": "0000000.00", "FOCUS": "0000000.00", "OFFSETX": "0000000.00",
                                  "OFFSETY": "0000000.00", "SCALINGX": "0000000.00", "SCALINGY": "0000000.00",
                                  "WFR_ROT": "0000000.00", "ORTHO": "0000000.00", "RET_SCALING": "0.083",
                                  "RET_ROT": "0.458", "EXP_MODE": None, "ENERGY_STEP": None, "FOCUS_STEP": None,
                                  "PROCESSINFO": None, "LOT_ID": "AP00005.01", "CARRIERID": "CPFE00005",
                                  "PRODUCTID": "0726P", "STAGENAME": "BP-DEP1", "STEPID": "BIFURINS2",
                                  "RUNCARDFLAG": 0}], "ResponseDatas": None}}

GET_backendCONTROLDATA = {
    "msgHead": {"traceId": "backendCS#20231228102823481", "rqstId": "20231228102823481", "srvName": "backend", "srvEnv": "Prod",
                "rqstAddr": None, "srvAddr": None, "service": "backendCS", "msgType": "R", "locale": None, "txId": 1,
                "rqstTime": "20231228102823481", "retCode": 0, "retMsg": ""},
    "msgBody": {"CMD": "GET_backendCONTROLDATA", "AREA": "PHOTO", "BATCHID": "20231228102823481", "EQPID": "ALST01",
                "RequestDatas": [{"EXPOSURE_RECIPE": "Flatness@TTT", "MASK": "M000101APLU1",
                                  "WAFERS": ["AP00005#04", "AP00005#03", "AP00005#02"], "LOT_ID": "AP00005",
                                  "CARRIERID": "CPFE00005", "PRODUCTID": "0726P", "STAGENAME": "BP-DEP1",
                                  "STEPID": "BIFURINS2", "RUNCARDFLAG": 0},
                                 {"EXPOSURE_RECIPE": "Flatnes1@TT1", "MASK": "M000101APLU1", "WAFERS": ["AP00005#01"],
                                  "LOT_ID": "AP00005.01", "CARRIERID": "CPFE00005", "PRODUCTID": "0726P",
                                  "STAGENAME": "BP-DEP1", "STEPID": "BIFURINS2", "RUNCARDFLAG": 0}],
                "ResponseDatas": None}}

import pika
import json
import uuid

response = None  # 全局变量用于存储响应


def xyn_product(product_data):
    #host = "10.32.206.5"
    host = "192.168.13.193"
    port = 5672
    message = json.dumps(product_data)
    byte_message = message.encode()
    connection_params = pika.ConnectionParameters(host=host, port=port)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.confirm_delivery()

    exchange_name = 'ex.mycim.backend.eap'
    routing_key = 'rk.mycim.backend.eap'

    result1 = channel.queue_declare(queue='', exclusive=True)
    callback_queue = result1.method.queue
    print(f"callback_queue:{callback_queue}")

    def on_response(ch, method, properties, body):
        print("on_response callback triggered")
        print(f"Received properties: {properties}")
        if properties.correlation_id == corr_id:
            global response
            response = body.decode()
            print("Received response:", response)
            channel.stop_consuming()
        else:
            print(f"Incorrect correlation_id. Expected: {corr_id}, Received: {properties.correlation_id}")

    # 发送消息
    corr_id = str(uuid.uuid4())
    print(f"Sending message with correlation_id: {corr_id}")

    channel.basic_publish(
        exchange=exchange_name,
        routing_key=routing_key,
        properties=pika.BasicProperties(
            reply_to=callback_queue,  # 指定回复队列
            correlation_id=corr_id
        ),
        body=byte_message
    )

    # 设置回调函数
    print(f"Setting up consumer to listen on queue: {callback_queue}")
    channel.basic_consume(queue=callback_queue, on_message_callback=on_response, auto_ack=True)

    # RPT_OV_MEASUREDATA
    print("Starting to consume")
    channel.start_consuming()

    connection.close()



# 测试函数
result = xyn_product(product_data=GET_backendCONTROLDATA)
#result = xyn_product(product_data=RPT_EXP_PROCESSSTART)
#result = xyn_product(product_data=RPT_EXP_PROCESSEND)
#result = xyn_product(product_data=RPT_CD_MEASUREDATA)
#result = xyn_product(product_data=RPT_OV_MEASUREDATA)

#result = xyn_product(product_data=product_data)
print("Processed result:", result)
