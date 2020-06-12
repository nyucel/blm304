#GizemÖzgün
#160401007

import sys
import os
import socket
from datetime import datetime
import time



class Client:
    def __init__(self, host, port):
        self.port = port
        self.host = host
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_connection(self):
        self.conn.connect((self.host, self.port))

    def setSystemTime(self, time):
	an = datetime.datetime.now()
	datetime.datetime.strftime(an, %'X')
        print(time)

    def start(self):
        self.start_connection()

        start = int(round(time.time() * 1000))

        self.conn.sendall("get_time".encode())
        data = self.conn.recv(4096)

        end = int(round(time.time() * 1000))

        total = end - start

        current_time = datetime.utcfromtimestamp((int(data.decode()) - total)/1000.0)
        self.setSystemTime(current_time)


if __name__ == '__main__':
    client = Client(sys.argv[1], int(sys.argv[2]))

    client.start()
