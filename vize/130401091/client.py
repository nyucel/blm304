# Emin Sekmenoglu 130401091
import socket, json, os, base64
from json import JSONEncoder


class Cevap:
    def __init__(self, session_id, method, credentials=None, data=None, result=None):
        self.protocol = 'FTP'
        self.version = '1.0'
        self.session_id = session_id
        self.method = method
        self.credentials = credentials
        self.data = data
        self.result = result


class KimlikBilgileri:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Veri:
    def __init__(self, data_id, is_last, header=None, content=None):
        self.data_id = data_id
        self.is_last = is_last
        self.header = header
        self.content = content


class FtpResult:
    def __init__(self, code, description):
        self.code = code
        self.description = description


class MesajtoJson(JSONEncoder):
    def default(self, o):
        return o.__dict__


class FtpClient:
    limitasyon = 100000

    def __init__(self, server_address, server_port, username, password):
        self.host = (server_address, server_port)
        self.username = username
        self.password = password
        self.session_id = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect(self.host)

    def send(self, data):
        self.sock.send(data)

    def receive(self, timeout=None):
        self.sock.settimeout(timeout)
        received_data = None

        while True:
            try:
                data = self.sock.recv(self.limitasyon)
            except socket.timeout:
                break

            received_data = data.decode()
            break

        return received_data

    def handle(self, received_data):
        cevap = json.loads(received_data)
        method = cevap['method']
        data = cevap['data']
        result = cevap['result']

        return method, data, result

    def next_session_id(self):
        self.session_id += 1
        return self.session_id

    def command_ls(self):
        kimlik_bilgileri = KimlikBilgileri(self.username, self.password)
        cevap = Cevap(self.next_session_id(), "ls", kimlik_bilgileri)

        jsoncevap = MesajtoJson().encode(cevap).encode()
        self.send(jsoncevap)

        content_ls = []

        while True:
            received_data = self.receive(5)

            if received_data is None:
                print('Cevap Yok')
                break

            method, data, result = self.handle(received_data)

            if result['code'] != 200:
                print('Error Code: {}'.format(result['code']))
                break

            if data['is_last']:
                content_ls += data['content'].split(';')

                for file in content_ls:
                    print(file)

                break

            content_ls += data['content'].split(';')

    # Implementation of command 'cd' : change directory in the remote server
    def command_cd(self, folder):
        kimlik_bilgileri = KimlikBilgileri(self.username, self.password)
        veri = Veri(1, True, header=folder)
        cevap = Cevap(self.next_session_id(), "cd", kimlik_bilgileri, veri)

        jsoncevap = MesajtoJson().encode(cevap).encode()
        self.send(jsoncevap)

        received_data = self.receive(5)

        if received_data is None:
            print('Cevap Yok')
            return

        method, data, result = self.handle(received_data)

        if result['code'] != 200:
            print('Error: {}'.format(result['code']))
        else:
            print('Basarili')

    # Implementation of command 'get' : get file from the remote server
    def command_get(self, filename):
        kimlik_bilgileri = KimlikBilgileri(self.username, self.password)
        veri = Veri(1, True, header=filename)
        cevap = Cevap(self.next_session_id(), "Get", kimlik_bilgileri, veri)

        jsoncevap = MesajtoJson().encode(cevap).encode()
        self.send(jsoncevap)

        content_get = bytearray()

        while True:
            received_data = self.receive(5)

            if received_data is None:
                print('Cevap Yok')
                break

            method, data, result = self.handle(received_data)

            if result['code'] != 200:
                print('Error: {}'.format(result['code']))
                break

            if data['is_last']:
                write_file(filename, content_get)
                print('Basarili')
                break
            else:
                content_get += base64.b64decode(data['content'])

    def command_put(self, filename):
        if os.path.isfile(filename):
            did = 1
            session_id = self.next_session_id()

            with open(filename, mode='rb') as file:
                while True:
                    file_content = file.read(1024)

                    if not file_content:
                        kimlik_bilgileri = KimlikBilgileri(self.username, self.password)
                        veri = Veri(did, True, header=filename, content="")
                        cevap = Cevap(session_id, "Put", kimlik_bilgileri, veri)
                        jsoncevap = MesajtoJson().encode(cevap).encode()

                        self.send(jsoncevap)

                        received_data = self.receive(5)

                        if received_data is None:
                            print('Cevap Yok')
                            break

                        method, data, result = self.handle(received_data)

                        if result['code'] != 200:
                            print('Error: {}'.format(result['code']))
                            break

                        print('Basarili')
                        break

                    b64_content = base64.b64encode(file_content).decode()

                    kimlik_bilgileri = KimlikBilgileri(self.username, self.password)
                    veri = Veri(did, False, header=filename, content=b64_content)
                    cevap = Cevap(session_id, "Put", kimlik_bilgileri, veri)

                    jsoncevap = MesajtoJson().encode(cevap).encode()

                    self.send(jsoncevap)
                    did += 1

                    received_data = self.receive(5)

                    if received_data is None:
                        print('Cevap yok')
                        break

                    method, data, result = self.handle(received_data)

                    if result['code'] != 200:
                        print('Error: {}'.format(result['code']))
                        break
        else:
            print('Dosya Bulunamadi')


def read_file(filename):
    with open(filename, mode='rb') as file:
        file_content = file.read()

    return file_content


def write_file(filename, file_content):
    with open(filename, 'wb') as file:
        file.write(file_content)


if __name__ == "__main__":
    ftpClient = FtpClient('localhost', 42, username="test", password="test")

    while True:
        command = input('> ')
        command_tokens = command.split()

        if not command_tokens:
            continue

        command = command_tokens[0].lower()

        if command == 'ls':
            ftpClient.command_ls()
        elif command == 'cd':
            if len(command_tokens) == 2:
                param = command_tokens[1]
                ftpClient.command_cd(param)
            else:
                print('Hatali Komut')
        elif command == 'get':
            if len(command_tokens) == 2:
                param = command_tokens[1]
                ftpClient.command_get(param)
            else:
                print('Hatali Komut')
        elif command == 'put':
            if len(command_tokens) == 2:
                param = command_tokens[1]
                ftpClient.command_put(param)
            else:
                print('Hatali Komut')