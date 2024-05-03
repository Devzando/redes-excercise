import socket

HOST = '127.0.0.1'  
PORT = 3333 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((HOST, PORT))
    while True:
        message = input("Cliente: ")
        s.sendall(message.encode())
        data = s.recv(1024)
        print('Servidor:', data.decode())
