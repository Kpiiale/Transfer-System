import pika
import os
import json
from Config import settings
from datetime import datetime

# Este consumidor escucha mensajes filtrados por tipo de usuario y banco (ej: "cliente.banco1")
def start_topic_consumer(binding_key):
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials
    ))

    channel = connection.channel()

    # Creamos un nombre de cola basado en el binding_key
    queue_name = f"topic_{binding_key.replace('.', '_')}"

    # Declaramos el exchange tipo topic
    channel.exchange_declare(exchange=settings.EXCHANGE_TOPIC, exchange_type='topic', durable=True)

    # Declaramos y enlazamos la cola al patrón (binding_key)
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=settings.EXCHANGE_TOPIC, queue=queue_name, routing_key=binding_key)

    logs_dir = os.path.join("logs")
    os.makedirs(logs_dir, exist_ok=True)

    def callback(ch, method, properties, body):
        try:
            message = json.loads(body.decode())
        except json.JSONDecodeError:
            message = {"raw": body.decode()}

        print(f"[Topic] Mensaje recibido ({binding_key}):")
        print(json.dumps(message, indent=2))

        # Guardamos el mensaje en un archivo separado por clave
        log_file_path = os.path.join(logs_dir, f"topic_{binding_key.replace('.', '_')}.log")
        with open(log_file_path, "a") as log_file:
            log_file.write(json.dumps(message) + "\n")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
