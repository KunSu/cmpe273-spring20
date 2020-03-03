# Author: Kun Su
# Code and Comment reference: https://docs.python.org/3/howto/sockets.html
import socket
from threading import Thread
import threading

TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024


def Client_Thread(clientsocket):
    while True:
        data = clientsocket.recv(BUFFER_SIZE)
        if not data:
            break

        print(f"Received data: {data.decode()}")
        clientsocket.sendall("pong".encode())

    clientsocket.close()


def listen_forever():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # use TCP_IP = 'localhost' or '127.0.0.1' which only visible within the same machine
    # use TCP_IP = socket.gethostname() will be visible to the outside world.
    serversocket.bind((TCP_IP, TCP_PORT))
    serversocket.listen(5)  # The number of max connection

    print('Server started at port 5000.')

    # 3 general ways to handle socket
    # 1. dispatching a thread to handle clientsocket
    # 2. create a new process to handle clientsocket
    # 3. restructure this app to use non-blocking sockets
    while True:
        # accept connections from outside
        try:
            clientsocket, address = serversocket.accept()
        except (KeyboardInterrupt, InterruptedError):
            break

        print(f'Connected Client:{address}')

        thread = threading.Thread(target=Client_Thread, args=(clientsocket,))
        thread.setDaemon(True)
        thread.start()

    serversocket.close()


listen_forever()
