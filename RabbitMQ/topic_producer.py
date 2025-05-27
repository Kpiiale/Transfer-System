import pika
import json
from Config import settings

def send_account_alert(routing_key, receipt_obj):
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials
    ))
    channel = connection.channel()

    channel.exchange_declare(exchange=settings.EXCHANGE_TOPIC, exchange_type='topic', durable=True)
    channel.basic_publish(
        exchange=settings.EXCHANGE_TOPIC,
        routing_key=routing_key,
        body=json.dumps(receipt_obj).encode()
    )

    print(f"[Topic] Alerta enviada a '{routing_key}': {receipt_obj}")
    connection.close()
