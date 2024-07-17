import socket
import threading
import os

def handle_client(client_socket, client_address):
    print(f"[+] Conexão aceita de {client_address}")
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("[-] Conexão encerrada")
                break
            elif message.startswith("FILE:"):
                filename = message.split(":")[1]
                receive_file(client_socket, filename)
            else:
                print(f"Cliente: {message}")
        except ConnectionResetError:
            print("[-] Conexão perdida")
            break
    
    client_socket.close()

def send_file(client_socket, filename):
    if os.path.exists(filename):
        client_socket.send(f"FILE:{filename}".encode('utf-8'))
        with open(filename, 'rb') as f:
            while chunk := f.read(1024):
                client_socket.send(chunk)
        print("[+] Arquivo enviado")
    else:
        print("[-] Arquivo não encontrado")

def receive_file(client_socket, filename):
    with open(f"received_{filename}", 'wb') as f:
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            f.write(chunk)
    print(f"[+] Arquivo {filename} recebido")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(1)
    print("[*] Servidor ouvindo na porta 9999")
    
    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    main()
