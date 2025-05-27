from Models.transaction import Transaction

class TransactionManager:
    def __init__(self):
        self.transactions = []

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
        print(f"Transferencia #{transaction_id} creada.")
        return transaction

    def get_transactions_by_account(self, account_number):
        return [t for t in self.transactions if t.from_account == account_number or t.to_account == account_number]

    def get_all_transactions(self):
        return self.transactions
