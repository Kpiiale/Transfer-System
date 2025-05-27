import pika  # Librería para trabajar con RabbitMQ
import os    # Para crear carpetas
import json  # Para leer mensajes en formato JSON
from Config import settings
from datetime import datetime

# Este consumidor escucha mensajes del exchange tipo DIRECT y los guarda en un archivo específico por usuario.
def start_direct_consumer(username):
    # Credenciales para conectarse a RabbitMQ
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)

    # Establecemos la conexión con RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials
    ))

    # Creamos el canal para comunicarnos
    channel = connection.channel()

    # Declaramos el exchange de tipo direct (mensajes dirigidos a usuarios específicos)
    channel.exchange_declare(exchange=settings.EXCHANGE_DIRECT, exchange_type='direct')

    # Creamos una cola única para este usuario
    queue_name = f"direct_{username}"
    channel.queue_declare(queue=queue_name, durable=True)

    # Enlazamos la cola al exchange con el nombre del usuario como routing_key
    channel.queue_bind(exchange=settings.EXCHANGE_DIRECT, queue=queue_name, routing_key=username)

    # Creamos el directorio de logs si no existe
    logs_dir = os.path.join("logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Esta función se ejecuta cuando llega un nuevo mensaje
    def callback(ch, method, properties, body):
        try:
            message = json.loads(body.decode())  # Convertimos el mensaje a un diccionario
        except json.JSONDecodeError:
            message = {"raw": body.decode()}  # En caso de error, lo guardamos como texto

        print(f"[Direct] {username} recibió:")
        print(json.dumps(message, indent=2))  # Imprime el mensaje bonito

        # Guardamos el mensaje en un archivo de log del usuario
        log_file_path = os.path.join(logs_dir, f"direct_{username}.log")
        with open(log_file_path, "a") as log_file:
            log_file.write(json.dumps(message) + "\n")

    # Le decimos a RabbitMQ que use nuestra función para procesar mensajes
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    # Comenzamos a escuchar mensajes (esto es bloqueante)
    channel.start_consuming()
