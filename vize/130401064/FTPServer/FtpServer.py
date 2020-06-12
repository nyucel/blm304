
import socket
import json
import logging
import os
import base64

from concurrent.futures import ThreadPoolExecutor
from time import sleep

from FtpMessage import FtpMessage
from FtpMessage import FtpData
from FtpMessage import FtpMessageEncoder
from FtpMessage import FtpResult


class FtpServer:
    MAX_BYTES = 65536

    def __init__(self, port):
        logging.info('Initializing FTP Server')
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', port))
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
        logging.info('Sent data to client %s: %s', address, data.decode())

    def listen(self):
        while True:
            data, address = self.sock.recvfrom(self.MAX_BYTES)
            logging.info('Received data from client %s: %s', address, data.decode())
            received_data = data.decode()
            self.executor.submit(self.handle, received_data, address)
            # thread = threading.Thread(target=self.handle, args=(received_data, address,))
            # thread.start()

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

        # Handle 'ls' command : list all files in the current working directory
        if method == 'List':
            file_data = ""
            prefix = ""
            files = [f for f in os.listdir(client_cwd)]

            for f in files:
                file_data += prefix
                file_data += f
                prefix = ";"

            response_data = create_response(ftp_message['session_id'], method, 200, content=file_data)
            # print(response_data)

            self.send(response_data, address)

        # Handle 'cd' command : change the current working directory
        elif method == 'ChangeDirectory':
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
                        response_data = create_response(ftp_message['session_id'], method, 200, data_id=did, is_last=False, header=file_name, content=b64_content)
                        self.send(response_data, address)
                        did += 1
                        sleep(0.05)

                response_data = create_response(ftp_message['session_id'], method, 200,
                                                data_id=did, is_last=True, header=file_name, content="")

                self.send(response_data, address)
            else:
                response_data = create_response(ftp_message['session_id'], method, 404, header=file_name)
                self.send(response_data, address)

        # Handle 'put' command : put the file to the server
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
    ftp_result = FtpResult(result_code, "")
    ftp_data = FtpData(data_id, is_last, header, content)
    ftp_message = FtpMessage(session_id, method, data=ftp_data, result=ftp_result)

    ftp_message_data = FtpMessageEncoder().encode(ftp_message).encode()

    return ftp_message_data


def read_file(filename):
    with open(filename, mode='rb') as file:
        file_content = file.read()

    return file_content


def write_file(filename, file_content):
    with open(filename, 'wb') as file:
        file.write(file_content)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)

    ftpServer = FtpServer(42)
    ftpServer.listen()

