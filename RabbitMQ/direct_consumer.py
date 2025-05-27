import pika
import os
from Config import settings
from datetime import datetime

def start_direct_consumer(username):
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials
    ))
    channel = connection.channel()

    channel.exchange_declare(exchange=settings.EXCHANGE_DIRECT, exchange_type='direct')
    queue_name = f"direct_{username}"
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=settings.EXCHANGE_DIRECT, queue=queue_name, routing_key=username)

    logs_dir = os.path.join("logs")
    transfers_dir = os.path.join("transfers")
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(transfers_dir, exist_ok=True)

    def callback(ch, method, properties, body):
        message = body.decode()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[Direct] {username} received: {message}")

        with open(os.path.join(logs_dir, f"direct_{username}.log"), "a") as log_file:
            log_file.write(f"[{timestamp}] {message}\n")

        with open(os.path.join(transfers_dir, f"{username}_transfers.txt"), "a") as tx_file:
            tx_file.write(f"[{timestamp}] {message}\n")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
