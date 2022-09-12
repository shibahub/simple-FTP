import socket

host = '127.0.0.1'
port = 9090
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect((host,port))
print(f'\033[1;31;40mConnecting to {host}:{port}......')
data = "Hello Server!"

clientSocket.send(data.encode())

 

# Receive data from server

dataFromServer = clientSocket.recv(1024)

 

# Print to the console

print(dataFromServer.decode('utf-8'))

clientSocket.close()
