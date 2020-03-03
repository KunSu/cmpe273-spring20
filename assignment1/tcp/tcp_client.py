import socket
import time
import argparse

TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024
MESSAGE = "ping"


def send(args):
    id = args[0]
    delay = args[1]
    number = args[2]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

    for count in range(number):
        time.sleep(delay)
        print("Sending data:", MESSAGE)
        s.send(f"{id}:{MESSAGE}".encode())
        data = s.recv(BUFFER_SIZE)
        print("Recevied data:", data.decode())

    s.close()


def get_client_id():
    parser = argparse.ArgumentParser()

    parser.add_argument('--id', type=str, help="[client id]")
    parser.add_argument('--delay', default=1, type=int,
                        help="[delay in seconds between messages]")
    parser.add_argument('--number', default=60, type=int,
                        help="[number of 'ping' messages]")

    args = parser.parse_args()
    id = args.id
    delay = args.delay
    number = args.number

    return id, delay, number


send(get_client_id())
