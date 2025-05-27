class Account:
    def __init__(self, account_id, owner_username, balance):
        self.account_id = account_id
        self.owner_username = owner_username
        self.balance = balance

    def __str__(self):
        return f"Cuenta {self.account_id}: {self.owner_username}, Fondos: ${self.balance:.2f}"
