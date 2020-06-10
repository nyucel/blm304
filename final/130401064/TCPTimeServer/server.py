# süleyman baltacý 130401064
import time
import datetime
import socket
from concurrent.futures import ThreadPoolExecutor


class TimeServer:
    def __init__(self, port):
        self.host = 'localhost'
        self.port = port
        self.executor = ThreadPoolExecutor(10)

    def task(self, connection):
        with connection:
            data = connection.recv(4096)

            utc_data = readfile('utc.txt').replace('UTC', '')
            milliseconds = int(round((time.time() * 1000)))
            send_data = "{}:{};{}:{}".format('Time', milliseconds, 'UTC', utc_data)

            print('Gonderilen zaman bilgisi: {}, UTC: {}'.format(datetime.datetime.utcfromtimestamp(milliseconds / 1000.0),utc_data))
            connection.sendall(send_data.encode())

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen()

            while True:
                connection, address = sock.accept()

                future = self.executor.submit(self.task, connection)


def readfile(filename):
    file = open(filename, mode='r')
    data = file.read()
    file.close()

    return data


if __name__ == '__main__':
    timeServer = TimeServer(142)

    timeServer.run()
