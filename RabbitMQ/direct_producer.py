import pika
from Config import settings

def send_transaction_confirmation(username, message):
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
        body=message.encode()
    )

    print(f"[Direct] Confirmacion enviada a {username}: {message}")
    connection.close()
