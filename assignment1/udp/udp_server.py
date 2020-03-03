import socket
import select
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 4000
BUFFER_SIZE = 1024
TIMEOUT = 3
FILE_NAME = "download.txt"


def listen_forever():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print('Server started at port 4000.')

    count = 0
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        if data:
            print('Accepting a file upload...')

        f = open(FILE_NAME, 'wb')

        while True:

            ready = select.select([sock], [], [], TIMEOUT)
            if ready[0]:
                data, addr = sock.recvfrom(BUFFER_SIZE)
                row_data = data.decode(encoding="utf-8")
                row_data = str.split(row_data, ",")
                acknowledgement = int(row_data[0]) + 1
                f.write(row_data[1].encode())
                sock.sendto(str(acknowledgement).encode(), addr)

            else:
                print('Upload successfully completed.')
                f.close()
                break


listen_forever()
