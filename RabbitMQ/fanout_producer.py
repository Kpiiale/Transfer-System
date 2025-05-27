import pika
import json
from Config import settings

def broadcast_notification(receipt_obj):
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials
    ))
    channel = connection.channel()

    channel.exchange_declare(exchange=settings.EXCHANGE_FANOUT, exchange_type='fanout')
    channel.basic_publish(
        exchange=settings.EXCHANGE_FANOUT,
        routing_key='',
        body=json.dumps(receipt_obj).encode()
    )

    print(f"[Fanout] Notificación enviada: {receipt_obj}")
    connection.close()
