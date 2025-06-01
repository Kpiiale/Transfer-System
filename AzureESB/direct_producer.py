import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage


with open("AzureESB/config_esb.json") as f:
    config = json.load(f)

CONN_STR = config["connection_string"]
QUEUE_NAME = "tareas"

def send_transaction_confirmation(username, message_dict):
    try:
        with ServiceBusClient.from_connection_string(CONN_STR) as client:
            sender = client.get_queue_sender(QUEUE_NAME)
            with sender:
                message_dict["username"] = username
                body = json.dumps(message_dict)
                message = ServiceBusMessage(body)
                sender.send_messages(message)
                print(f"[Azure ESB] Mensaje enviado para {username}")
    except Exception as e:
        print("[Error] No se pudo enviar mensaje por Azure:", e)
