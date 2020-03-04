import socket
import time
import random

UDP_IP = "127.0.0.1"
UDP_PORT = 4000
BUFFER_SIZE = 1024
TIMEOUT = 1
FILE_NAME = "upload.txt"


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(FILE_NAME.encode(), (UDP_IP, UDP_PORT))
sock.settimeout(TIMEOUT)

if sock:
    print('Connected to the server.')

ack_id = random.randint(0, 10000)

f = open(FILE_NAME, "r")
data = f.read(BUFFER_SIZE)
if data:
    print('Starting a file ({}) upload...'.format(FILE_NAME))

while(data):
    message = "{},{}".format(ack_id, data).encode()
    if sock.sendto(message, (UDP_IP, UDP_PORT)):
        data = f.read(BUFFER_SIZE)
        # time.sleep(0.02)

    acknowledgement = False
    while(not acknowledgement):
        try:
            acknowledgement_id, _ = sock.recvfrom(BUFFER_SIZE)
            acknowledgement_id = int(
                acknowledgement_id.decode(encoding="utf-8"))
            if acknowledgement_id == ack_id + 1:
                acknowledgement = True

        except socket.error:
            print('Package lost, resending...')
            sock.sendto(message, (UDP_IP, UDP_PORT))

    print('Received ack({}) from the server.'.format(acknowledgement_id))
    ack_id = acknowledgement_id + 1


sock.close()
f.close()
print('File upload successfully completed.')
