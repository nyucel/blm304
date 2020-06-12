import socket
from datetime import datetime, timezone, timedelta
# 170401016

class Server:
    def __init__(self, timezone=0, buffersize=256, server_ip):
        self.host = '0.0.0.0'  # socket.gethostbyname(socket.gethostname())
        self.port = 142
        self.buffer_size = buffersize
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.time_zone = timezone
        self.conn = None
        self.conn_addr = None

    def connect(self):
        print('istemci bekleniyor...')
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        self.conn, self.conn_addr = self.server_socket.accept()
        print('connected.')

    def get_current_time(self):
        time = datetime.utcnow()
        time += timedelta(hours=self.time_zone)

        return time

    def append_timezone(self, time):
        return str(time) + '[@]UTC ' + str(self.time_zone)

    def calculate_delay(self):
        time_to_send = self.get_current_time()

        self.conn.send(str(time_to_send).encode())

        client_response = self.conn.recv(self.buffer_size)

        time_now = self.get_current_time()

        delay = (time_now - time_to_send) / 2
        return delay

    def listen(self):
        self.connect()

        while True:
            message = self.conn.recv(self.buffer_size).decode()

            if not message or message == 'Q':
                self.conn.close()
                break

            elif message == 'S':
                delay = self.calculate_delay()

                current_time = self.get_current_time() + delay

                current_time_with_utc_str = self.append_timezone(current_time)

                self.conn.send(current_time_with_utc_str.encode())
                print(f'{current_time_with_utc_str} istemciye gonderildi.')


print('serverin kullanmasini istedigi UTC degerini giriniz.')
print('Ornek olarak 3 girmeniz UTC +3 e, -2 girmeniz UTC-2 ye karsilik gelecektir.')
time_zone = int(input('UTC:'))

server = Server(timezone=time_zone)

server.listen()
