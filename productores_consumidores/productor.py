import json

import random
from datetime import datetime, timezone
from azure.servicebus import ServiceBusClient, ServiceBusMessage

with open("config.json") as f:
    config = json.load(f)

conn_str = config["SERVICE_BUS_CONNECTION_STR"]
queue_name = config["QUEUE_NAME"]

def generar_alerta_sensor():
    tipo = random.choice(["temperatura", "presion", "vibracion"])
    umbrales = {"temperatura": 90.0, "presion": 150.0, "vibracion": 5.0}
    valor = round(random.uniform(umbrales[tipo], umbrales[tipo] + 10), 2)

    return {
        "device_id": f"sensor-{random.randint(1000, 9999)}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": tipo,
        "value": valor,
        "threshold": umbrales[tipo],
        "status": "ALERTA",
        "location": random.choice(["Planta 1", "Planta 2", "Planta 3"])
    }

alerta = generar_alerta_sensor()

servicebus_client = ServiceBusClient.from_connection_string(conn_str)
with servicebus_client:
    sender = servicebus_client.get_queue_sender(queue_name=queue_name)
    with sender:
        message = ServiceBusMessage(json.dumps(alerta))
        sender.send_messages(message)
        print("Alerta enviada:", alerta)
