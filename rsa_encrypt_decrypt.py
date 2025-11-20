from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# -----------------------------
# GENERATE KEYS
# -----------------------------
def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    # Save keys to files
    with open("private_key.pem", "wb") as f:
        f.write(private_key)

    with open("public_key.pem", "wb") as f:
        f.write(public_key)

    print("[+] Keys generated: private_key.pem & public_key.pem")


# -----------------------------
# ENCRYPT TEXT FILE
# -----------------------------
def encrypt_file(input_file: str, output_file: str):
    # Read plaintext
    with open(input_file, "r", encoding="utf-8") as f:
        plaintext = f.read()

    # Load public key
    with open("public_key.pem", "rb") as f:
        public_key = RSA.import_key(f.read())

    cipher = PKCS1_OAEP.new(public_key)

    # RSA can only encrypt small chunks (~190 bytes), suitable for small text
    ciphertext = cipher.encrypt(plaintext.encode())

    # Save encrypted data
    with open(output_file, "wb") as f:
        f.write(ciphertext)

    print(f"[+] Encrypted and saved to {output_file}")


# -----------------------------
# DECRYPT ENCRYPTED FILE
# -----------------------------
def decrypt_file(input_file: str, output_file: str):
    # Load private key
    with open("private_key.pem", "rb") as f:
        private_key = RSA.import_key(f.read())

    cipher = PKCS1_OAEP.new(private_key)

    # Read ciphertext
    with open(input_file, "rb") as f:
        ciphertext = f.read()

    # Decrypt
    plaintext = cipher.decrypt(ciphertext).decode()

    # Save decrypted text
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(plaintext)

    print(f"[+] Decrypted text saved to {output_file}")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    print("1. Generate RSA Keys")
    print("2. Encrypt text file")
    print("3. Decrypt encrypted file")

    choice = input("Enter choice: ")

    if choice == "1":
        generate_keys()
    elif choice == "2":
        encrypt_file("plaintext.txt", "encrypted.bin")
    elif choice == "3":
        decrypt_file("encrypted.bin", "decrypted.txt")
    else:
        print("Invalid choice.")
