import socket
import struct
import os
import sys
import json

from numpy import spacing


host = '127.0.0.1'
port = 9090
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def listfile():
    try:
       
        print('Index  File               Size')
        leng=clientSocket.recv(1)
        leng=leng.decode('utf-8')
        leng=int(leng)
        #print(leng)
        for i in range(leng):
            #print(i)
            #data=clientSocket.req
            data = clientSocket.recv(1)
            #print(data)
            lenI=data.decode('utf-8')
            lenI=int(lenI)
            #print(lenI)
            data=clientSocket.recv(lenI)
            data=data.decode('utf-8')
            size=clientSocket.recv(2)
            size=size.decode('utf-8')
            print(f'{i}.    {data}                {size}')
    except:
        print ("Could not found the file, some error occur")
    return

def dowload():
    try:
        inp= input('>Please INput file name: ')
        clientSocket.send(inp.encode('utf-8'))
        res=clientSocket.recv(14) # problem with size
        print(res.decode('utf-8'))
        with open(inp+'2', 'wb') as f:
            print ('file opened')
            while True:
                print('receiving data...')
                data = clientSocket.recv(1024)
                print(data)
                #print('shiba')
                #print('data=', (data))
                f.write(data)
                if not data:
                    break
                break
    
    except:
        print ("Could not found the file, some error occur")
    return
    
def upload():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        file_name = input(">Enter file name: ")
        try:
            #If file exceed 2MB according to ajarn
            if os.path.getsize(file_name) < 2097152:
                #กุส่งเป็น json ทำไมวะ ขกแก้ละ LOL
                dt = {
                    "file_name": file_name 
                }
                dts = json.dumps(dt)
                s.send(dts.encode())
                #Send file's data
                fname = file_name
                f = open(fname, 'rb')
                l = f.read(2048)
                while (l) :
                    s.send(l)
                    l = f.read(2048)
                f.close()
                s.close()
            else :
                print('FILE SIZE EXCEED 2MB')
        except:
            s.close()
            print("no such file")    


try: 
    clientSocket.connect((host,port))
    print(f'\033[1;32;40mConnecting to {host}:{port}......')
    dataFromServer = clientSocket.recv(1024)    
    while True:
            
        print(dataFromServer.decode('utf-8'))
        data=input('>command: ')
        if data=='ls':
            print('<============== LIST OF FILE ==============>')
            clientSocket.send(data.encode('utf-8'))   
            listfile()
        if data=='d':
            print('<============== DOWNLOAD ==============>')   
            clientSocket.send(data.encode('utf-8')) 
            dowload()
        if data=='u':
            print('<============== UPLOAD ==============>')   
            clientSocket.send(data.encode('utf-8')) 
            upload()
        elif data=='q':
            clientSocket.send(data.encode('utf-8'))
            clientSocket.close()
            break
        else:
            #data=input('command: ')
            print ('please try again')
          
except:
    print('error occur')
    clientSocket.close()

clientSocket.close()