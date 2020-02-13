# Author: Kun Su
# Code and Comment reference: https://docs.python.org/3/howto/sockets.html
import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024

def listen_forever():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # use TCP_IP = 'localhost' or '127.0.0.1' which only visible within the same machine
    # use TCP_IP = socket.gethostname() will be visible to the outside world.
    serversocket.bind((TCP_IP, TCP_PORT)) 
    serversocket.listen(5) # The number of max connection 

    while True:
        # accept connections from outside
        (clientsocket, address) = serversocket.accept()
        if clientsocket:
            print(f'Connection address:{address}')

            data = clientsocket.recv(BUFFER_SIZE)
            print(f"received data: {data.decode()}")
            clientsocket.send("pong".encode())

    clientsocket.close()

listen_forever()