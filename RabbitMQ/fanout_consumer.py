import pika
import os
from Config import settings
from datetime import datetime

def start_fanout_consumer():
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials
    ))
    channel = connection.channel()

    channel.exchange_declare(exchange=settings.EXCHANGE_FANOUT, exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=settings.EXCHANGE_FANOUT, queue=queue_name)

    logs_dir = os.path.join("logs")
    os.makedirs(logs_dir, exist_ok=True)

    def callback(ch, method, properties, body):
        message = body.decode()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[Fanout] Received broadcast: {message}")
        with open(os.path.join(logs_dir, "fanout.log"), "a") as log_file:
            log_file.write(f"[{timestamp}] {message}\n")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
