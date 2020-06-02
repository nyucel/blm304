# Emin Sekmenoglu 130401091
import socket, json, os, base64
from json import JSONEncoder
from concurrent.futures import ThreadPoolExecutor
from time import sleep


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


class Kontrol:
    def __init__(self, code, description):
        self.code = code
        self.description = description


class CevaptoJson(JSONEncoder):
    def default(self, o):
        return o.__dict__


class FtpServer:
    limitasyon = 1000000

    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('localhost', port))
        self.clients = {}
        self.client_cwd = {}
        self.client_data = {}
        self.executor = ThreadPoolExecutor(10)
        self.init()

    def init(self):
        with open('password.txt') as file:
            content = file.readlines()

        lines = [line.strip() for line in content]

        for line in lines:
            parts = line.split(':', 2)
            cwd = os.getcwd().replace('\\', '/')
            self.clients[parts[0]] = parts[1]
            self.client_cwd[parts[0]] = cwd
            self.client_data[parts[0]] = []

    def send(self, data, address):
        self.sock.sendto(data, address)

    def listen(self):
        while True:
            data, address = self.sock.recvfrom(self.limitasyon)
            received_data = data.decode()
            self.executor.submit(self.handle, received_data, address)

    def handle(self, received_data, address):
        ftp_message = json.loads(received_data)
        method = ftp_message['method']
        credentials = ftp_message['credentials']
        data = ftp_message['data']
        result = ftp_message['result']

        if credentials['username'] not in self.clients:
            response_data = create_response(ftp_message['session_id'], method, 404)
            self.send(response_data, address)
            return

        password = self.clients[credentials['username']]

        if password != credentials['password']:
            response_data = create_response(ftp_message['session_id'], method, 403)
            self.send(response_data, address)
            return

        client_cwd = self.client_cwd[credentials['username']]

        if method == 'List':
            file_data = ""
            prefix = ""
            files = [f for f in os.listdir(client_cwd)]

            for f in files:
                file_data += prefix
                file_data += f
                prefix = ";"

            response_data = create_response(ftp_message['session_id'], method, 200, content=file_data)

            self.send(response_data, address)

        elif method == 'cd':
            folder = data['header']

            if folder == '.':
                result_code = 200
            elif folder == '..':
                dirs = client_cwd.replace('\\', '/').split('/')

                if len(dirs) > 2:
                    dirs.pop()
                    client_cwd = '/'.join(dirs)
                    self.client_cwd[credentials['username']] = client_cwd
                    result_code = 200
                else:
                    result_code = 403
            else:
                dirs = client_cwd.replace('\\', '/').split('/')

                dirs.append(folder)
                cwd = '/'.join(dirs)

                if os.path.isdir(cwd):
                    client_cwd = cwd
                    self.client_cwd[credentials['username']] = client_cwd
                    result_code = 200
                else:
                    result_code = 404

            response_data = create_response(ftp_message['session_id'], method, result_code, header=folder)

            self.send(response_data, address)

        # Handle 'get' command : get the file from the server
        elif method == 'Get':
            file_name = data['header']
            file_path = client_cwd + '/' + file_name

            if os.path.isfile(file_path):
                did = 1
                with open(file_path, mode='rb') as file:
                    while True:
                        file_content = file.read(1024)

                        if not file_content:
                            break

                        b64_content = base64.b64encode(file_content).decode()
                        response_data = create_response(ftp_message['session_id'], method, 200,
                                                        data_id=did, is_last=False, header=file_name, content=b64_content)
                        self.send(response_data, address)
                        did += 1
                        sleep(0.05)

                response_data = create_response(ftp_message['session_id'], method, 200,
                                                data_id=did, is_last=True, header=file_name, content="")

                self.send(response_data, address)
            else:
                response_data = create_response(ftp_message['session_id'], method, 404, header=file_name)
                self.send(response_data, address)

        elif method == 'Put':
            file_name = data['header']

            did = data['data_id']

            if did == 1:
                self.client_data[credentials['username']] = []

            if data['is_last']:
                content = bytearray()

                file_name = data['header']
                file_path = client_cwd + '/' + file_name

                for c in self.client_data[credentials['username']]:
                    content += c

                write_file(file_path, content)
            else:
                self.client_data[credentials['username']].append(base64.b64decode(data['content']))

            response_data = create_response(ftp_message['session_id'], method, 200, data_id=data['data_id'], header=file_name)
            self.send(response_data, address)

        # Not implemented command
        else:
            response_data = create_response(ftp_message['session_id'], method, 501)
            self.send(response_data, address)


def create_response(session_id, method, result_code, data_id=1, is_last=True, header=None, content=None):
    kontrol = Kontrol(result_code, "")
    veri = Veri(data_id, is_last, header, content)
    cevap = Cevap(session_id, method, data=veri, result=kontrol)

    jsoncevap = CevaptoJson().encode(cevap).encode()

    return jsoncevap


def read_file(filename):
    with open(filename, mode='rb') as file:
        file_content = file.read()

    return file_content


def write_file(filename, file_content):
    with open(filename, 'wb') as file:
        file.write(file_content)


if __name__ == "__main__":
    ftpServer = FtpServer(42)
    ftpServer.listen()

