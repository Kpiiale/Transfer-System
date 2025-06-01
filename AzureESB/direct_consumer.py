import json
from azure.servicebus import ServiceBusClient


with open("AzureESB/config_esb.json") as f:
    config = json.load(f)

CONN_STR = config["connection_string"]
QUEUE_NAME = "tareas"

def start_direct_consumer():
    try:
        with ServiceBusClient.from_connection_string(CONN_STR) as client:
            receiver = client.get_queue_receiver(QUEUE_NAME)
            with receiver:
                print("[Azure ESB] Escuchando mensajes...")
                for msg in receiver:
                    body = str(msg)
                    try:
                        data = json.loads(body)
                        print(f"[Azure ESB] Mensaje para {data.get('username')}:")
                        print(json.dumps(data, indent=4))
                    except:
                        print("[Azure ESB] Mensaje recibido:", body)
                    receiver.complete_message(msg)
    except Exception as e:
        print("[Error consumidor Azure]:", e)

if __name__ == "__main__":
    start_direct_consumer()
