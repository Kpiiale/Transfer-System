import json
import os
from Models.user import User
from Services.auth_service import login
from Services.transaction_manager import TransactionManager

USERS_FILE = "Data/users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        data = json.load(f)
        return [User(**user) for user in data]

def main_menu(user):
    tx_manager = TransactionManager()
    msg_service = MessageService()
    msg_service.start_for_user(user.username, user.account_type, user.bank_code)

    try:
        while True:
            print("\n1. Hacer transferencia")
            print("2. Ver mis transferencias")
            print("0. Salir")
            choice = input("Seleccionar opción: ")

            if choice == "1":
                from_acc = input("Desde la cuenta con ID: ")
                to_acc = input("Para la cuenta con ID: ")
                amount = float(input("Cantidad: "))
                tx = tx_manager.create_transaction(from_acc, to_acc, amount)
                print(tx)

            elif choice == "2":
                acc_id = input("Ingrese el ID de su cuenta: ")
                transactions = tx_manager.get_transactions_by_account(acc_id)
                for t in transactions:
                    print(t)

            elif choice == "0":
                print("Saliendo...")
                msg_service.stop_all()
                break
            else:
                print("Opcion Inválida.")
    except KeyboardInterrupt:
        print("\nInterrupcion. Desconectando consumidores...")
        msg_service.stop_all()

def main():
    while True:
        users = load_users()
        user = None
        while not user:
            user = login(users)
        main_menu(user)

if __name__ == "__main__":
    main()
