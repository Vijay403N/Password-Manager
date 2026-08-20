import os
import json
import base64
import hashlib
from cryptography.fernet import Fernet

DATA_FILE = "passwords.json"

def generate_key(master_password):
    # Derive a key from the master password
    digest = hashlib.sha256(master_password.encode()).digest()
    return base64.urlsafe_b64encode(digest)

def load_passwords():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_passwords(passwords):
    with open(DATA_FILE, "w") as f:
        json.dump(passwords, f, indent=2)

def add_password(passwords, service, username, password, fernet):
    encrypted = fernet.encrypt(password.encode()).decode()
    passwords[service] = {"username": username, "password": encrypted}
    save_passwords(passwords)
    print(f"Saved password for {service}")

def get_password(passwords, service, fernet):
    if service in passwords:
        encrypted = passwords[service]["password"]
        decrypted = fernet.decrypt(encrypted.encode()).decode()
        print(f"\nService: {service}")
        print("Username:", passwords[service]["username"])
        print("Password:", decrypted)
    else:
        print("No entry found for", service)

def main():
    master_password = input("Enter master password: ")
    key = generate_key(master_password)
    fernet = Fernet(key)

    passwords = load_passwords()

    while True:
        print("\n=== Password Manager ===")
        print("1. Add Password")
        print("2. Get Password")
        print("3. Exit")
        choice = input("Choose option: ")

        if choice == "1":
            service = input("Service name: ")
            username = input("Username: ")
            pwd = input("Password: ")
            add_password(passwords, service, username, pwd, fernet)
        elif choice == "2":
            service = input("Service name: ")
            get_password(passwords, service, fernet)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
