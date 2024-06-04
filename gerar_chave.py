from cryptography.fernet import Fernet

# Gera uma chave e a imprime
chave = Fernet.generate_key()
with open('.env', 'w') as file:
    file.write(f'SECRET_KEY={chave.decode()}\n')
print(f'Chave gerada e salva no arquivo .env: {chave.decode()}')
