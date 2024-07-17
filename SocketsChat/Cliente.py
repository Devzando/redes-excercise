import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith("FILE:"):
                filename = message.split(":")[1]
                receive_file(client_socket, filename)
            else:
                print(f"Servidor: {message}")
        except ConnectionResetError:
            print("[-] Conexão perdida")
            break

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
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))
    
    recv_thread = threading.Thread(target=receive_messages, args=(client,))
    recv_thread.start()
    
    while True:
        message = input("Você: ")
        if message.startswith("FILE:"):
            filename = message.split(":")[1]
            send_file(client, filename)
        else:
            client.send(message.encode('utf-8'))

if __name__ == "__main__":
    main()
