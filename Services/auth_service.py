def login(users):
    username = input("Usuario: ").strip()
    password = input("Contraseña: ").strip()

    for user in users:
        if user.username == username and user.password == password:
            print(f"Bienvenido {user.username} ({user.account_type})")
            return user
    print("Credenciales invalidas.")
    return None
