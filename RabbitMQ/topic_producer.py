import pika
from Config import settings

def send_account_alert(routing_key, message):
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials
    ))
    channel = connection.channel()

    channel.exchange_declare(exchange=settings.EXCHANGE_TOPIC, exchange_type='topic', durable=True)
    channel.basic_publish(exchange=settings.EXCHANGE_TOPIC, routing_key=routing_key, body=message.encode())

    print(f"[Topic] Alerta Mandada a '{routing_key}': {message}")
    connection.close()
