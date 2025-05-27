# Importamos las librerías necesarias
import json
import os
from datetime import datetime

# Importamos la clase que representa una transferencia
from Models.transaction import Transaction

# Importamos funciones que permiten enviar mensajes a través de RabbitMQ
from RabbitMQ.direct_producer import send_transaction_confirmation
from RabbitMQ.fanout_producer import broadcast_notification
from RabbitMQ.topic_producer import send_account_alert

# Ruta del archivo donde se guardarán las transferencias realizadas
TRANSACTION_FILE = "Data/transactions.json"

# Esta clase se encarga de gestionar las transferencias entre cuentas
class TransactionManager:

    def __init__(self):
        # Lista que almacena todas las transferencias
        self.transactions = []
        self.load_transactions()  # Cargamos las transferencias desde el archivo al iniciar

    # Cargar transferencias guardadas desde un archivo JSON
    def load_transactions(self):
        if os.path.exists(TRANSACTION_FILE):
            with open(TRANSACTION_FILE, "r") as f:
                data = json.load(f)
                # Convertimos los datos JSON a objetos Transaction
                self.transactions = [Transaction(**tx) for tx in data]
        else:
            self.transactions = []

    # Guardar todas las transferencias en el archivo JSON
    def save_transactions(self):
        with open(TRANSACTION_FILE, "w") as f:
            json.dump([t.__dict__ for t in self.transactions], f, indent=4)

    # Crear una nueva transferencia entre dos cuentas
    def create_transaction(self, from_account, to_account, amount, users):
        # Validaciones básicas antes de crear la transferencia
        if from_account == to_account:
            print("No puedes transferir a tu misma cuenta.")
            return None

        if amount <= 0:
            print("El monto debe ser mayor a cero.")
            return None

        if not any(u.account_number == to_account for u in users):
            print("La cuenta destino no existe.")
            return None

        # Creamos el objeto de la transferencia
        transaction_id = len(self.transactions) + 1
        transaction = Transaction(transaction_id, from_account, to_account, amount)
        self.transactions.append(transaction)
        self.save_transactions()  # Guardamos la nueva transferencia

        print(f"Transferencia #{transaction_id} creada.")

        # Obtenemos la hora actual como texto
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Buscamos los usuarios que participan en la transferencia
        to_user = next((u for u in users if u.account_number == to_account), None)
        from_user = next((u for u in users if u.account_number == from_account), None)

        # Creamos un comprobante base en formato JSON (diccionario)
        base_receipt = {
            "type": "transfer_receipt",
            "transaction_id": transaction_id,
            "from_account": from_account,
            "to_account": to_account,
            "amount": amount,
            "timestamp": timestamp
        }

        # Enviamos confirmación al usuario que hizo la transferencia (emisor)
        if from_user:
            sender_receipt = base_receipt.copy()
            sender_receipt["role"] = "sender"
            send_transaction_confirmation(from_user.username, sender_receipt)

        # Enviamos confirmación al receptor y alerta por topic
        if to_user:
            receiver_receipt = base_receipt.copy()
            receiver_receipt["role"] = "receiver"
            send_transaction_confirmation(to_user.username, receiver_receipt)

            # Enviamos alerta por routing_key al topic (por tipo y banco)
            routing_key = f"{to_user.account_type}.{to_user.bank_code}"
            alert_receipt = base_receipt.copy()
            alert_receipt["role"] = "notification"
            send_account_alert(routing_key, alert_receipt)

        # Notificamos a todos (fanout)
        fanout_receipt = base_receipt.copy()
        fanout_receipt["role"] = "notification"
        broadcast_notification(fanout_receipt)

        return transaction

    # Obtener todas las transferencias relacionadas con una cuenta específica
    def get_transactions_by_account(self, account_number):
        return [t for t in self.transactions if t.from_account == account_number or t.to_account == account_number]

    # Obtener todas las transferencias realizadas en general
    def get_all_transactions(self):
        return self.transactions
