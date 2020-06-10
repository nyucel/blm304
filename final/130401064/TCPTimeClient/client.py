# süleyman baltacý 130401064
import socket
import datetime
import win32api


class TimeClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))

            start_time = datetime.datetime.now()
            sock.sendall(b'Time')
            data = sock.recv(4096)
            finish_time = datetime.datetime.now()

            elapsed_time = finish_time - start_time
            one_way_time = elapsed_time / 2

        tokens = data.decode().split(';')
        millis = int(tokens[0].split(':')[1])
        utc = int(tokens[1].split(':')[1])

        d = datetime.datetime.utcfromtimestamp(millis/1000.0)
        delta = datetime.timedelta(minutes=utc*60)
        delta = delta + one_way_time
        d = d + delta
        print('Zaman bilgisi: {}'.format(d))
        win32api.SetSystemTime(d.year, d.month, d.weekday(), d.day, d.hour, d.minute, d.second, 0)


if __name__ == '__main__':
    timeClient = TimeClient('127.0.0.1', 142)

    timeClient.run()
