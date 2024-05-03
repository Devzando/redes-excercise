import socket

HOST = '127.0.0.1' 
PORT = 3333  


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))

    s.listen()
    print("Aguardando conexão do cliente...")

    conn, addr = s.accept()
    with conn:
        print('Conectado por', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print('Cliente:', data.decode())
            message = input("Servidor: ")
            conn.sendall(message.encode())