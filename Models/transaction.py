class Transaction:
    def __init__(self, transaction_id, from_account, to_account, amount):
        self.transaction_id = transaction_id
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount

    def __str__(self):
        return f"Transferencia {self.transaction_id}: ${self.amount:.2f} de {self.from_account} para {self.to_account}"
