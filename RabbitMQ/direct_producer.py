import pika
import json
from Config import settings

def send_transaction_confirmation(username, receipt_obj):
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials
    ))
    channel = connection.channel()

    channel.exchange_declare(exchange=settings.EXCHANGE_DIRECT, exchange_type='direct')
    channel.basic_publish(
        exchange=settings.EXCHANGE_DIRECT,
        routing_key=username,
        body=json.dumps(receipt_obj).encode()
    )

    print(f"[Direct] Confirmación enviada a {username}: {receipt_obj}")
    connection.close()
