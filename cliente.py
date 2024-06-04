import socket
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Chave de criptografia (carregada do arquivo .env)
chave = os.getenv('SECRET_KEY').encode()

cipher_suite = Fernet(chave)

def encrypt_message(message):
    return cipher_suite.encrypt(message.encode())

def decrypt_message(encrypted_message):
    return cipher_suite.decrypt(encrypted_message).decode()

def main():
    # Configuração do cliente
    host = '127.0.0.1'
    port = 1234

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Envia uma solicitação de leitura de estoque
    message = 'GET:1'
    client_socket.send(encrypt_message(message))
    encrypted_response = client_socket.recv(1024)
    response = decrypt_message(encrypted_response)
    print("Resposta do servidor:", response)

    # Envia uma solicitação de transferência de estoque
    message = 'TRANSFER:1:2:produtoA:50'
    client_socket.send(encrypt_message(message))
    encrypted_response = client_socket.recv(1024)
    response = decrypt_message(encrypted_response)
    print("Resposta do servidor:", response)

    client_socket.close()

if __name__ == "__main__":
    main()
