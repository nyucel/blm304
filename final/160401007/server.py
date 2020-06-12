#GizemÖzgün
#160401007

import os
import sys
import socket
from datetime import datetime
import time



class Server:
    def __init__(self, port, time_zone = "UTC+0"):
        self.host = '127.0.0.1'
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.time_zone = int(time_zone.split('+')[1])*60*60*1000

    def start_connection(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()

    def run(self):
        self.start_connection()
        while True:
            conn, address = self.socket.accept()

            data = conn.recv(4096)

            if data.decode() == "get_time":
                current_time = int(round(time.time() * 1000)) + self.time_zone
                conn.send(str(current_time).encode())


if __name__ == '__main__':
    if len(sys.argv) > 1:
        server = Server(142, sys.argv[1])
    else:
        server = Server(142)


    server.run()
