import pika

import json

def callback(ch, method, properties, body):
    message = json.loads(body)
    print("Received message:", message)
    # 在这里处理消息

# RabbitMQ 服务器连接参数
connection_parameters = pika.ConnectionParameters('localhost')  # 修改为你的RabbitMQ服务器地址
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

# 声明交换机和队列，确保它们与生产者使用的一致
exchange_name = 'ex.mycim.backend.eap'  # 修改为你的交换机名称
queue_name = 'cim.queue'        # 修改为你的队列名称
routing_key = 'your_routing_key'      # 修改为你的路由键

channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
channel.queue_declare(queue=queue_name)
channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key=routing_key)

# 开始消费
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
