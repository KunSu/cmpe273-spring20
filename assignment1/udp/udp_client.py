import socket
import time
import random

UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 1024
MESSAGE = "ping"

def send(id=0):
    
    for x in range(int(id)):
        unique_sequence_id = "{},{},{}".format(x, time.time(), random.randint(0, 10000))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(1.0)

            recv_acknowledgement = False
            s.sendto(f"SYN,{unique_sequence_id}".encode(), (UDP_IP, UDP_PORT))
            while(not recv_acknowledgement):
                # s.sendto(f"SYN,{unique_sequence_id}".encode(), (UDP_IP, UDP_PORT))
                # pre = time.time()
                data, ip = s.recvfrom(BUFFER_SIZE)
                print("{}: {}".format(ip, data.decode(encoding="utf-8").strip()))
                data = data.decode(encoding="utf-8").strip()

                if str.startswith(data, "ACK"):
                    syn = str.split(data, ",")
                    usi = str.split(unique_sequence_id, ",")
                    # print(syn)
                    # print(usi)

                    if syn[1] == usi[0] and syn[2] == usi[1] and int(syn[3]) == int(usi[2]) + 1:
                        recv_acknowledgement = True
                        ack = "{},{},{},{}".format(syn[1], syn[2], syn[3], int(syn[4]) + 1)
                        s.sendto(f"DATA,{ack},{MESSAGE}".encode(), (UDP_IP, UDP_PORT))
                        data, ip = s.recvfrom(BUFFER_SIZE)
                        print("received data: {}: {}".format(ip, data.decode()))

                else:
                # cur = time.time()
                # if cur - pre >= 1:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    s.sendto(f"SYN,{unique_sequence_id}".encode(), (UDP_IP, UDP_PORT))

            
        except socket.error:
            print("Error! {}".format(socket.error))
            s.sendto(f"SYN,{unique_sequence_id}".encode(), (UDP_IP, UDP_PORT))
            # exit()


def get_client_id():
    id = input("Enter client id:")
    return id

send(get_client_id())