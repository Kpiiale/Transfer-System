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
    
def create_user(users):
    print("\n=== Crear nuevo usuario ===")
    username = input("Nombre de usuario: ").strip()
    password = input("Contraseña: ").strip()
    account_number = input("Número de cuenta (único): ").strip()
    account_type = input("Tipo de cuenta (savings/checking): ").strip().lower()
    bank_code = input("Código del banco (bank1/bank2/...): ").strip().lower()

    if any(u.username == username or u.account_number == account_number for u in users):
        print("Usuario o número de cuenta ya existe.")
        return

    new_user = User(username, password, account_number, account_type, bank_code)
    users.append(new_user)

    # Guardar en JSON
    with open(USERS_FILE, "w") as f:
        json.dump([u.__dict__ for u in users], f, indent=4)
    print("Usuario creado exitosamente.")

def main_menu(user, users):
    tx_manager = TransactionManager()
    msg_service = MessageService()
    msg_service.start_for_user(user.username, user.account_type, user.bank_code)

    try:
        while True:
            print("\n--- MENÚ PRINCIPAL ---")
            if user.account_type == "admin":
                print("1. Crear nuevo usuario")
                print("2. Ver usuarios")
                print("0. Cerrar sesión")
                option = input("Selecciona una opción: ")

                if option == "1":
                    create_user(users)
                elif option == "2":
                    print("\n=== Usuarios registrados ===")
                    for u in users:
                        print(f"{u.username} | {u.account_number} | {u.account_type} | {u.bank_code}")
                elif option == "0":
                    print("Cerrando sesión...")
                    msg_service.stop_all()
                    break
                else:
                    print("Opción inválida.")

            else:
                print("1. Realizar transferencia")
                print("2. Ver mis transferencias")
                print("0. Cerrar sesión")
                option = input("Selecciona una opción: ")

                if option == "1":
                    from_acc = user.account_number
                    to_acc = input("Número de cuenta destino: ").strip()
                    amount = float(input("Monto a transferir: "))
                    tx = tx_manager.create_transaction(from_acc, to_acc, amount)
                    print(f"Transferencia realizada: {tx}")

                elif option == "2":
                    transactions = tx_manager.get_transactions_by_account(user.account_number)
                    print("\n=== Historial de transferencias ===")
                    for t in transactions:
                        print(t)

                elif option == "0":
                    print("Cerrando sesión...")
                    msg_service.stop_all()
                    break
                else:
                    print("Opción inválida.")
    except KeyboardInterrupt:
        print("\nSesión interrumpida. Cerrando consumidores...")
        msg_service.stop_all()

def main():
    while True:
        users = load_users()
        user = None
        while not user:
            print("\n=== INICIO DE SESIÓN ===")
            user = login(users)
        main_menu(user, users)
if __name__ == "__main__":
    main()
