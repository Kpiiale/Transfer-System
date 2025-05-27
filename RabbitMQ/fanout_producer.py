import pika
from Config import settings

def broadcast_notification(message):
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials
    ))
    channel = connection.channel()

    channel.exchange_declare(exchange=settings.EXCHANGE_FANOUT, exchange_type='fanout')
    channel.basic_publish(exchange=settings.EXCHANGE_FANOUT, routing_key='', body=message.encode())

    print(f"[Fanout] Notificacion enviada: {message}")
    connection.close()
