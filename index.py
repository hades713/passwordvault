import json
import getpass
from cryptography.fernet import Fernet
import sys

def generate_key():
    key = Fernet.generate_key()
    try:
        with open("encryption_key.txt", "wb") as file:
            file.write(key)
    except IOError:
        print("Error: Unable to open the encryption_key.txt file.")
        sys.exit(1)
    return key

def load_key():
    try:
        with open("encryption_key.txt", "rb") as file:
            key = file.read()
            return key
    except FileNotFoundError:
        print("Encryption key file not found. Generating a new key...")
        key = generate_key()
        return key

def encrypt_password(password, key):
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, key):
    cipher_suite = Fernet(key)
    decrypted_password = cipher_suite.decrypt(encrypted_password)
    return decrypted_password.decode()

def save_passwords(passwords):
    try:
        with open("passwords.txt", "w") as file:
            json.dump(passwords, file, default=lambda x: x.decode() if isinstance(x, bytes) else x)
    except IOError:
        print("Error: Unable to open the passwords.txt file.")
        sys.exit(1)

def load_passwords():
    try:
        with open("passwords.txt", "r") as file:
            passwords = json.load(file)
            return passwords
    except (IOError, json.JSONDecodeError):
        print("Error: Unable to load passwords from the passwords.txt file.")
        return {}

def add_password():
    website = input("Enter the website: ")
    username = input("Enter the username: ")
    password = getpass.getpass("Enter the password: ")

    passwords = load_passwords()
    passwords[website] = {
        "username": username,
        "password": encrypt_password(password, key)
    }
    save_passwords(passwords)
    print("Password added successfully.")

def list_passwords():
    passwords = load_passwords()
    if passwords:
        print("Passwords:")
        for website, data in passwords.items():
            print(f"Website: {website}")
            print(f"Username: {data['username']}")
            decrypted_password = decrypt_password(data['password'], key)
            print(f"Password: {decrypted_password}")
            print("--------------------")
    else:
        print("No passwords found.")

def delete_password(website):
    passwords = load_passwords()
    if website in passwords:
        del passwords[website]
        save_passwords(passwords)
        print("Password deleted successfully.")
    else:
        print("Website not found in passwords.")

def update_password(website):
    passwords = load_passwords()
    if website in passwords:
        username = input("Enter the new username: ")
        password = getpass.getpass("Enter the new password: ")
        passwords[website]["username"] = username
        passwords[website]["password"] = encrypt_password(password, key)
        save_passwords(passwords)
        print("Password updated successfully.")
    else:
        print("Website not found in passwords.")

key = load_key()

if not key:
    key = generate_key()

master_password = getpass.getpass("Enter your master password: ")

encrypted_master_password = encrypt_password(master_password, key)

try:
    with open("master_password.txt", "wb") as file:
        file.write(encrypted_master_password)
except IOError:
    print("Error: Unable to open the master_password.txt file.")
    sys.exit(1)

while True:
    print("Menu:")
    print("1. Add Password")
    print("2. List Passwords")
    print("3. Delete Password")
    print("4. Update Password")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_password()
    elif choice == "2":
        list_passwords()
    elif choice == "3":
        website = input("Enter the website to delete the password: ")
        delete_password(website)
    elif choice == "4":
        website = input("Enter the website to update the password: ")
        update_password(website)
    elif choice == "5":
        sys.exit(0)
    else:
        print("Invalid choice. Please try again.")