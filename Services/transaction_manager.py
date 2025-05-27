from Models.transaction import Transaction

class TransactionManager:
    def __init__(self):
        self.transactions = []

    def create_transaction(self, from_account, to_account, amount):
        transaction_id = len(self.transactions) + 1
        transaction = Transaction(transaction_id, from_account, to_account, amount)
        self.transactions.append(transaction)
        print(f"Transaction #{transaction_id} created.")
        return transaction

    def get_transactions_by_account(self, account_id):
        return [t for t in self.transactions if t.from_account == account_id or t.to_account == account_id]

    def get_all_transactions(self):
        return self.transactions
