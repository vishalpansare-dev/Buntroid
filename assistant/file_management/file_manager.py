import os
import time
import shutil
import hashlib
from cryptography.fernet import Fernet

# Configuration
SOURCE_DIR = "files_to_manage/"
ARCHIVE_DIR = "archived_files/"
AGE_LIMIT_DAYS = 30  # For deleting old files
ENCRYPTION_KEY_PATH = "encryption.key"

# Encryption setup (using cryptography library)
def generate_encryption_key():
    """
    Generate a new encryption key and save it to a file.
    """
    key = Fernet.generate_key()
    with open(ENCRYPTION_KEY_PATH, "wb") as key_file:
        key_file.write(key)
    print("Encryption key generated and saved.")

def encrypt_file(file_path):
    """
    Encrypt a file using Fernet encryption.
    """
    try:
        with open(ENCRYPTION_KEY_PATH, "rb") as key_file:
            key = key_file.read()
        cipher = Fernet(key)

        with open(file_path, "rb") as file:
            file_data = file.read()

        encrypted_data = cipher.encrypt(file_data)

        encrypted_file_path = file_path + ".enc"
        with open(encrypted_file_path, "wb") as enc_file:
            enc_file.write(encrypted_data)

        print(f"File {file_path} encrypted successfully.")
    except Exception as e:
        print(f"Error encrypting file {file_path}: {str(e)}")

def decrypt_file(file_path):
    """
    Decrypt an encrypted file using the stored key.
    """
    try:
        with open(ENCRYPTION_KEY_PATH, "rb") as key_file:
            key = key_file.read()
        cipher = Fernet(key)

        with open(file_path, "rb") as file:
            encrypted_data = file.read()

        decrypted_data = cipher.decrypt(encrypted_data)

        decrypted_file_path = file_path.replace(".enc", "")
        with open(decrypted_file_path, "wb") as dec_file:
            dec_file.write(decrypted_data)

        print(f"File {file_path} decrypted successfully.")
    except Exception as e:
        print(f"Error decrypting file {file_path}: {str(e)}")

def rename_files():
    """
    Rename files in the directory by adding a timestamp and removing special characters.
    """
    try:
        for filename in os.listdir(SOURCE_DIR):
            file_path = os.path.join(SOURCE_DIR, filename)
            if os.path.isfile(file_path):
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                new_filename = timestamp + "_" + "".join(e for e in filename if e.isalnum() or e == '.')
                new_file_path = os.path.join(SOURCE_DIR, new_filename)
                os.rename(file_path, new_file_path)
                print(f"Renamed {filename} to {new_filename}")
    except Exception as e:
        print(f"Error in renaming files: {str(e)}")

def delete_old_files():
    """
    Delete files older than the specified age limit from the directory.
    """
    try:
        current_time = time.time()

        for filename in os.listdir(SOURCE_DIR):
            file_path = os.path.join(SOURCE_DIR, filename)
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                file_age_days = file_age / (60 * 60 * 24)

                if file_age_days > AGE_LIMIT_DAYS:
                    os.remove(file_path)
                    print(f"Deleted old file: {filename}")
    except Exception as e:
        print(f"Error deleting old files: {str(e)}")

if __name__ == "__main__":
    generate_encryption_key()
    encrypt_file("test.txt")  # Example file encryption
    decrypt_file("test.txt.enc")  # Example file decryption
    rename_files()
    delete_old_files()
