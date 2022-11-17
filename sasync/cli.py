#bug

import asyncio
from asyncio import StreamReader, StreamWriter
import os

REMOTE_ADDRESS = '127.0.0.1'
REMOTE_PORT = 5050


async def listfile(reader):
    data = await reader.read(100)
    data = data.decode('utf-8')
    print(data)

    return


async def download(reader,writer):
    filename = input('Enter file name to download:')

    writer.write(filename.encode('utf-8'))
    await writer.drain()

    ack = await reader.read(100)
    ack = ack.decode('utf-8')

    if ack == 'ack' :
        print(ack)
        stream = await reader.read(9999999999999999999999999999999999999999999999999999999999)

        with open(filename, 'wb') as f:
            f.write(stream)

        print("download finished")

    return


async def upload(writer):
    filename = input('Enter file name to upload:')
    
    if os.path.isfile(filename):

        writer.write(filename.encode('utf-8'))
        await writer.drain()

        with open(filename, 'rb') as f:
            l = f.read()
        writer.write(l)
        await writer.drain()
        

    return

async def main():
    try:
        reader, writer = await asyncio.open_connection(REMOTE_ADDRESS, REMOTE_PORT)
        while True:
            print('********************************************')
            data = input('command:')
            if data == 'ls':
                print('<============== LIST OF FILE ==============>')
                writer.write(data.encode('utf8'))
                
                #await writer.drain()
                await listfile(reader)

            if data == 'dwn':
                print('<================ DOWNLOAD ================>')
                writer.write(data.encode('utf8'))
                await download(reader,writer)

            if data == 'up':
                print('<================= UPLOAD =================>')
                writer.write(data.encode('utf8'))
                await upload(writer)


    except ConnectionRefusedError:
        print(f'Failed to connect to {REMOTE_ADDRESS}:{REMOTE_PORT}')
    except ConnectionResetError:
        print(f'Server is down')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass