import threading

import pika

from app.utils import SettingsTMP


class BrockerM:
    channel = None
    connection = None
    factory = None
    consumerThread = None

    def lifeCheck(self):
        try:
            if self.connection:
                return [True,"brocker"]
            return [False,"brocker"]
        except (Exception) as e:
            return [e,"broker"]

    def __init__(self, FactoryObj):
        print("!###############!!"+SettingsTMP.RABBITMQ_HOST)
        self.factory = FactoryObj
        # Устанавливаем соединение с RabbitMQ
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=SettingsTMP.RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=SettingsTMP.RABBITMQ_QUEUE_post)
        self.channel.queue_declare(queue=SettingsTMP.RABBITMQ_QUEUE_get)

    def send_message(self, message):
        self.channel.basic_publish(exchange='', routing_key=SettingsTMP.RABBITMQ_QUEUE_post, body=message)
        print(f" [x] Sent message: {message}")

    # Функция для получения сообщений из очереди
    def receive_messages(self):
        # Подпишемся на очередь
        # auto_ack=True -- no matter if lost
        self.channel.basic_consume(queue=SettingsTMP.RABBITMQ_QUEUE_get, on_message_callback=self.callback,
                                   auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    # Callback для обработки сообщения
    def start_consuming(self):
        print("start consuming")
        self.consumerThread = threading.Thread(target=self.receive_messages)
        self.consumerThread.start()


    def callback(self, ch, method, properties, body):
        print(f" [x] Received message: {body.decode()}")
        tmp = body.decode()
        tmp = self.factory.execute_command(tmp)

        if tmp:
            self.send_message(str(tmp))

    def __del__(self):
        try:
            self.connection.close()
        except:
            print("connection = none")
