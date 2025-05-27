import json
import os
from Models.transaction import Transaction
from RabbitMQ.direct_producer import send_transaction_confirmation
from RabbitMQ.fanout_producer import broadcast_notification
from RabbitMQ.topic_producer import send_account_alert

TRANSACTION_FILE = "Data/transactions.json"

class TransactionManager:
    def __init__(self):
        self.transactions = []
        self.load_transactions()

    def load_transactions(self):
        if os.path.exists(TRANSACTION_FILE):
            with open(TRANSACTION_FILE, "r") as f:
                data = json.load(f)
                self.transactions = [Transaction(**tx) for tx in data]
        else:
            self.transactions = []

    def save_transactions(self):
        with open(TRANSACTION_FILE, "w") as f:
            json.dump([t.__dict__ for t in self.transactions], f, indent=4)

    def create_transaction(self, from_account, to_account, amount, users):
        if from_account == to_account:
            print("No puedes transferir a tu misma cuenta.")
            return None

        if amount <= 0:
            print("El monto debe ser mayor a cero.")
            return None

        if not any(u.account_number == to_account for u in users):
            print("La cuenta destino no existe.")
            return None

        transaction_id = len(self.transactions) + 1
        transaction = Transaction(transaction_id, from_account, to_account, amount)
        self.transactions.append(transaction)
        self.save_transactions()

        print(f"Transferencia #{transaction_id} creada.")
        message = f"Transferencia #{transaction_id}: ${amount:.2f} de {from_account} para {to_account}"

        # Buscar usuarios involucrados
        to_user = next((u for u in users if u.account_number == to_account), None)
        from_user = next((u for u in users if u.account_number == from_account), None)

        if to_user:
            # Confirmación al receptor (Direct)
            send_transaction_confirmation(to_user.username, message)

            # Alerta por tipo y banco (Topic)
            routing_key = f"{to_user.account_type}.{to_user.bank_code}"
            send_account_alert(routing_key, message)

        if from_user:
            # Confirmación al emisor (Direct)
            send_transaction_confirmation(from_user.username, message)

            # También podría enviarle alerta por topic si deseas
            routing_key = f"{from_user.account_type}.{from_user.bank_code}"
            send_account_alert(routing_key, f"Has enviado: {message}")

        # Fanout para todos
        broadcast_notification(message)

        return transaction


    def get_transactions_by_account(self, account_number):
        return [t for t in self.transactions if t.from_account == account_number or t.to_account == account_number]

    def get_all_transactions(self):
        return self.transactions
