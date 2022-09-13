import socket

host = '127.0.0.1'
port = 9090
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect((host,port))
print(f'\033[1;32;40mConnecting to {host}:{port}......')
dataFromServer = clientSocket.recv(1024)
print(dataFromServer.decode('utf-8'))
data=input('')
clientSocket.send(data.encode('utf-8'))




clientSocket.close()
