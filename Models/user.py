class User:
    def __init__(self, username, password, account_type, bank_code):
        self.username = username
        self.password = password
        self.account_type = account_type  
        self.bank_code = bank_code     

    def __str__(self):
        return f"{self.username} ({self.account_type}, {self.bank_code})"
