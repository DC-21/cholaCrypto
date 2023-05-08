import string
import random
import os
from cryptography.fernet import Fernet

KEY_FILE = 'key.key'

def choice():
    action = input("Do you want to encrypt or decrypt? Enter 'e' for encryption or 'd' for decryption: ")
    return action

def generate_password(length=16):
    """Generate a random password of the specified length."""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def generate_key(password):
    """Generate a Fernet key from the specified password."""
    key = Fernet.generate_key()
    f = Fernet(key)
    token = f.encrypt(password.encode())
    return key, token

def save_key(key):
    """Save the key to a file."""
    with open(KEY_FILE, 'wb') as f:
        f.write(key)

def load_key():
    """Load the key from a file."""
    with open(KEY_FILE, 'rb') as f:
        key = f.read()
    return key

def encrypt_file(file_path, key):
    """Encrypt the specified file using the specified key."""
    with open(file_path, 'rb') as f:
        data = f.read()
    f = Fernet(key)
    encrypted = f.encrypt(data)
    with open(file_path + '.enc', 'wb') as f:
        f.write(encrypted)

def decrypt_file(file_path, key):
    """Decrypt the specified file using the specified key."""
    with open(file_path, 'rb') as f:
        data = f.read()
    f = Fernet(key)
    decrypted = f.decrypt(data)
    with open(file_path[:-4], 'wb') as f:
        f.write(decrypted)

# Example usage:
password = generate_password()
print('Generated password:', password)

key, token = generate_key(password)
print('Generated key:', key)

file_path = 'demo.txt'

encrypt_file(file_path, key)
print('File encrypted.')

action = choice()

if action == 'e':
    save_key(key)
elif action == 'd':
    if os.path.exists(KEY_FILE):
        key = load_key()
        decrypt_file(file_path + '.enc', key)
        print('File decrypted.')
    else:
        print('Encryption key not found. Cannot decrypt file.')
else:
    print("Invalid choice, please enter 'e' for encryption or 'd' for decryption.")
