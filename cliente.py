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

    # Loop para enviar solicitações de estoque e transferências
    while True:
        # Opções do usuário
        print("\nOpções:")
        print("1. Solicitar leitura de estoque")
        print("2. Solicitar transferência de estoque")
        print("3. Sair")

        opcao = input("Escolha uma opção (1/2/3): ")

        # Solicitar leitura de estoque
        if opcao == '1':
            loja_id = input("Digite o ID da loja: ")
            message = f'GET:{loja_id}'
            client_socket.send(encrypt_message(message))
            encrypted_response = client_socket.recv(1024)
            response = decrypt_message(encrypted_response)
            print("Resposta do servidor:", response)

        # Solicitar transferência de estoque
        elif opcao == '2':
            loja_origem = input("Digite o ID da loja de origem: ")
            loja_destino = input("Digite o ID da loja de destino: ")
            produto = input("Digite o nome do produto: ")
            quantidade = input("Digite a quantidade a ser transferida: ")
            message = f'TRANSFER:{loja_origem}:{loja_destino}:{produto}:{quantidade}'
            client_socket.send(encrypt_message(message))
            encrypted_response = client_socket.recv(1024)
            response = decrypt_message(encrypted_response)
            print("Resposta do servidor:", response)

        # Sair do cliente
        elif opcao == '3':
            print("Encerrando o cliente...")
            break

        else:
            print("Opção inválida. Escolha novamente.")

    client_socket.close()

if __name__ == "__main__":
    main()
