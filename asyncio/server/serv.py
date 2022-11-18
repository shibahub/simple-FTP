import asyncio
from asyncio import StreamReader, StreamWriter
import os
import sys 

REMOTE_ADDRESS = '127.0.0.1'
REMOTE_PORT = 5050


def ls(writer) :
    print ("Listing directory")

    txt = ''
    for x in os.listdir():
        txt += f'{x}\n'

    writer.write(txt.encode('utf-8'))
    
    
    return


async def dwn(reader, writer) :
    fname = await reader.read(100)
    fname = fname.decode('utf-8')

    if os.path.isfile(fname):
        writer.write('ack'.encode('utf-8'))
        #####
        await writer.drain()
        print(f'DOWNLOAD FILE: {fname}')
        f = open(fname,'rb')
        l = f.read()

        writer.write(l)

    else :
        writer.write('noack'.encode('utf-8'))
        await writer.drain()
        print('FILE NAME NOT EXIST')

    return

async def up(reader):
    fname = await reader.read(100)
    fname = fname.decode('utf-8')

    stream = await reader.read(999999999999999999999999999)
    with open(fname, 'wb') as f:
        f.write(stream)
    print(f'UPLOAD FILE: {fname}')

    return


async def handle(reader: StreamReader, writer: StreamWriter):
    while True:

        data = await reader.read(100)  # Max byte to read.
        data = data.decode('utf-8')

        if data == 'ls' :
            ls(writer)
        
        if data == 'dwn' :
            await dwn(reader,writer)

        if data == 'up' :
            await up(reader)

        sender_address, sender_port = writer.get_extra_info('peername')
        print(f'CONNECTED TO: {sender_address} ON PORT: {sender_port}')

        #writer.write('testing'.encode('utf8'))
        #await writer.drain()
    #writer.close()


async def main(host: str, port: int):
    print(f'Listening to {REMOTE_ADDRESS} on port: {REMOTE_PORT}')

    server = await asyncio.start_server(handle, host, port)
    await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main(REMOTE_ADDRESS, REMOTE_PORT))
    except KeyboardInterrupt:
        pass