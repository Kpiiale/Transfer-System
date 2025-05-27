import pika
import os
import json
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
    os.makedirs(logs_dir, exist_ok=True)

    def callback(ch, method, properties, body):
        try:
            message = json.loads(body.decode())
        except json.JSONDecodeError:
            message = {"raw": body.decode()}

        print(f"[Direct] {username} recibió:")
        print(json.dumps(message, indent=2))

        log_file_path = os.path.join(logs_dir, f"direct_{username}.log")
        with open(log_file_path, "a") as log_file:
            log_file.write(json.dumps(message) + "\n")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
