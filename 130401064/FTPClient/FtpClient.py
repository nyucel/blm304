
import socket
import json
import os
import base64
# import logging

from time import sleep

from FtpMessage import FtpMessage
from FtpMessage import FtpCredentials
from FtpMessage import FtpData
from FtpMessage import FtpMessageEncoder


class FtpClient:
    MAX_BYTES = 65536

    def __init__(self, server_address, server_port, username, password):
        # logging.info('Initializing FTP Client')
        self.host = (server_address, server_port)
        self.username = username
        self.password = password
        self.session_id = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect(self.host)

    def send(self, data):
        # print("Sending {}".format(data))
        self.sock.send(data)

    def receive(self, timeout=None):
        self.sock.settimeout(timeout)
        received_data = None

        while True:
            try:
                data = self.sock.recv(self.MAX_BYTES)
                # print(data)
            except socket.timeout:
                break

            received_data = data.decode()
            # print(received_data)
            break

        return received_data

    def handle(self, received_data):
        ftp_message = json.loads(received_data)
        method = ftp_message['method']
        data = ftp_message['data']
        result = ftp_message['result']

        return method, data, result

    def next_session_id(self):
        self.session_id += 1
        return self.session_id

    # Implementation of command 'ls' : list files in the remote server
    def command_ls(self):
        ftp_credentials = FtpCredentials(self.username, self.password)
        ftp_message = FtpMessage(self.next_session_id(), "List", ftp_credentials)

        ftp_message_data = FtpMessageEncoder().encode(ftp_message).encode()
        self.send(ftp_message_data)

        content_ls = []

        while True:
            received_data = self.receive(5)

            if received_data is None:
                print('Error on receive')
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
        ftp_credentials = FtpCredentials(self.username, self.password)
        ftp_data = FtpData(1, True, header=folder)
        ftp_message = FtpMessage(self.next_session_id(), "ChangeDirectory", ftp_credentials, ftp_data)

        ftp_message_data = FtpMessageEncoder().encode(ftp_message).encode()
        self.send(ftp_message_data)

        received_data = self.receive(5)

        if received_data is None:
            print('Error: No response received')
            return

        method, data, result = self.handle(received_data)

        if result['code'] != 200:
            print('Error: {}'.format(result['code']))
        else:
            print('Done')

    # Implementation of command 'get' : get file from the remote server
    def command_get(self, filename):
        ftp_credentials = FtpCredentials(self.username, self.password)
        ftp_data = FtpData(1, True, header=filename)
        ftp_message = FtpMessage(self.next_session_id(), "Get", ftp_credentials, ftp_data)

        ftp_message_data = FtpMessageEncoder().encode(ftp_message).encode()
        self.send(ftp_message_data)

        content_get = bytearray()

        while True:
            received_data = self.receive(5)

            if received_data is None:
                print('Error: No response received')
                break

            method, data, result = self.handle(received_data)

            if result['code'] != 200:
                print('Error: {}'.format(result['code']))
                break

            if data['is_last']:
                write_file(filename, content_get)
                print('Done')
                break
            else:
                content_get += base64.b64decode(data['content'])

    # Implementation of command 'put' : put local file to the remote server
    def command_put(self, filename):
        if os.path.isfile(filename):
            did = 1
            session_id = self.next_session_id()

            with open(filename, mode='rb') as file:
                while True:
                    file_content = file.read(1024)

                    if not file_content:
                        ftp_credentials = FtpCredentials(self.username, self.password)
                        ftp_data = FtpData(did, True, header=filename, content="")
                        ftp_message = FtpMessage(session_id, "Put", ftp_credentials, ftp_data)
                        ftp_message_data = FtpMessageEncoder().encode(ftp_message).encode()

                        self.send(ftp_message_data)

                        received_data = self.receive(5)

                        if received_data is None:
                            print('Error: No response received')
                            break

                        method, data, result = self.handle(received_data)

                        if result['code'] != 200:
                            print('Error: {}'.format(result['code']))
                            break

                        print('Done')
                        break

                    b64_content = base64.b64encode(file_content).decode()

                    ftp_credentials = FtpCredentials(self.username, self.password)
                    ftp_data = FtpData(did, False, header=filename, content=b64_content)
                    ftp_message = FtpMessage(session_id, "Put", ftp_credentials, ftp_data)

                    ftp_message_data = FtpMessageEncoder().encode(ftp_message).encode()

                    self.send(ftp_message_data)
                    did += 1

                    received_data = self.receive(5)

                    if received_data is None:
                        print('Error: No response received')
                        break

                    method, data, result = self.handle(received_data)

                    if result['code'] != 200:
                        print('Error: {}'.format(result['code']))
                        break
        else:
            print('Error: File not found')


def read_file(filename):
    with open(filename, mode='rb') as file:
        file_content = file.read()

    return file_content


def write_file(filename, file_content):
    with open(filename, 'wb') as file:
        file.write(file_content)


if __name__ == "__main__":
    # logging.getLogger().setLevel(logging.DEBUG)

    ftpClient = FtpClient('127.0.0.1', 42, username="user1", password="pass1")

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
                print('Command error')
        elif command == 'get':
            if len(command_tokens) == 2:
                param = command_tokens[1]
                ftpClient.command_get(param)
            else:
                print('Command error')
        elif command == 'put':
            if len(command_tokens) == 2:
                param = command_tokens[1]
                ftpClient.command_put(param)
            else:
                print('Command error')

