import json
from azure.servicebus import ServiceBusClient

with open("config.json") as f:
    config = json.load(f)

conn_str = config["SERVICE_BUS_CONNECTION_STR"]
queue_name = config["QUEUE_NAME"]

servicebus_client = ServiceBusClient.from_connection_string(conn_str)

with servicebus_client:
    receiver = servicebus_client.get_queue_receiver(queue_name=queue_name, max_wait_time=10)
    with receiver:
        for msg in receiver:
            alerta = json.loads(str(msg))
            print("\n Alerta recibida:")
            print(f"Sensor: {alerta['device_id']}")
            print(f"Ubicación: {alerta['location']}")
            print(f"Tipo: {alerta['type']} | Valor: {alerta['value']} > Umbral: {alerta['threshold']}")
            print(f"Tiempo: {alerta['timestamp']}")
            receiver.complete_message(msg)
