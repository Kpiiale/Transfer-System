import json
import os
from Models.transaction import Transaction

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
        return transaction

    def get_transactions_by_account(self, account_number):
        return [t for t in self.transactions if t.from_account == account_number or t.to_account == account_number]

    def get_all_transactions(self):
        return self.transactions
