import socket
import random

UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 1024
MESSAGE = "pong"
map = {}

def listen_forever():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", UDP_PORT))

    count = 0
    while True:
        count += 1
        
        # get the data sent to us
        data, ip = s.recvfrom(BUFFER_SIZE)

        if count >= 100:
            count = 0
        else:

            ack_id = random.randint(0, 10000)
            print("{}: {}".format(ip, data.decode(encoding="utf-8").strip()))
            data = data.decode(encoding="utf-8").strip()
            syn = str.split(data, ",")

            if str.startswith(data, "SYN"):
                ack = "ACK,{},{},{},{}".format(syn[1], syn[2], int(syn[3]) + 1, ack_id)
                # print(ack)
                key = "{},{}".format(syn[1], syn[2])
                map[key] = ack_id
                s.sendto(ack.encode(), ip)
            elif str.startswith(data, "DATA"):
                print(data)
                key = "{},{}".format(syn[1], syn[2])
                ack_id = map[key]
                if ack_id + 1 == int(syn[4]):
                    s.sendto(MESSAGE.encode(), ip)

        # reply back to the client
        # s.sendto(MESSAGE.encode(), ip)


listen_forever()