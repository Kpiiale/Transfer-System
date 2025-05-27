def login(users):
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    for user in users:
        if user.username == username and user.password == password:
            print(f"Welcome {user.username} ({user.account_type})")
            return user
    print("Invalid credentials.")
    return None
