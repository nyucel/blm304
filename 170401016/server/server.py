# 170401016 - Can Sözbir
import socket
import os
import base64
import sys
import random


def generate_random(n):
    return random.randrange(2**(n - 1), 2**n)


class Server:
    def __init__(self, directory='./files/'):
        self.ip = socket.gethostname()
        self.port = 42
        self.buffer_size = 1024
        self.directory = directory
        self.server_socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_DGRAM
        )
        self.server_socket.bind((self.ip, self.port))
        print(self.port, 'dinleniyor...')
        self.connected = False

    def listen(self):
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)

        print('Bir baglanti yapilmasi bekleniyor...')

        while not self.connected:
            client_seq, address = self.server_socket.recvfrom(
                self.buffer_size)

            client_seq = int(client_seq.decode())

            ack = client_seq + 1

            seq = generate_random(32)

            self.server_socket.sendto(
                (str(ack) + str(seq)).encode(), address)

            response, address = self.server_socket.recvfrom(
                self.buffer_size)

            response = response.decode()
            last_ack, last_seq = response[:10], response[10:]

            print(last_ack, seq, last_seq, ack)
            if int(last_ack) == seq + 1 and int(last_seq) == ack:
                self.connected = True

        print('Baglanti basarili bir sekilde saglandi.')

        while True:
            message, address = self.server_socket.recvfrom(self.buffer_size)

            message = message.decode()

            if message == 'ls':
                print(f'{address} den ls istegi alindi.')

                ls = os.listdir(self.directory)
                ls = str(ls)[1:-1].replace(',', '\n')

                self.server_socket.sendto(
                    ls.encode(), address)

            else:
                splitted = message.split(' ')
                command, argument = splitted[0], ' '.join(splitted[1:])

                if command == 'put':

                    print(f'{address} den put istegi alindi.')
                    self.server_socket.sendto(
                        "Put istegi server tarafindan alindi.".encode(), address)

                    with open(self.directory + argument, 'wb+') as newfile:
                        data, address = self.server_socket.recvfrom(
                            self.buffer_size)

                        while b"<@EOF@>" not in data:
                            writedata = data[10:]
                            newfile.write(writedata)

                            seq = int(data[:10].decode())
                            ack = seq + 1

                            self.server_socket.sendto(
                                str(ack).encode(), address)

                            data, address = self.server_socket.recvfrom(
                                self.buffer_size)
                    print(argument, f' dosyasi {address} tarafindan yuklendi.')

                elif command == 'get':

                    print(f'{address} den get istegi alindi.')
                    self.server_socket.sendto(
                        "Get istegi server tarafindan alindi.".encode(), address)

                    seq = generate_random(32)

                    with open(self.directory+argument, 'rb') as sendfile:
                        data = sendfile.read(self.buffer_size-10)
                        while data:

                            self.server_socket.sendto(
                                str(seq).encode()+data, address)

                            self.server_socket.settimeout(2)
                            try:
                                received = self.server_socket.recvfrom(
                                    self.buffer_size)
                                ack = int(received[0].decode())

                                if ack == seq + 1:
                                    seq = ack
                                    data = sendfile.read(self.buffer_size-10)

                            except:
                                print('Dosya gonderilirken baglanti hatasi,',
                                      'server.py ve client.py yi yeniden baslatip dosyayi tekrar gonderiniz ...')

                                self.connected = False
                                return
                    self.server_socket.sendto(
                        str(seq).encode()+b"<@EOF@>", address)
                    self.server_socket.settimeout(None)


# istersek sunucunun kullanacagi dosya yolunu degistirebiliriz
server = Server(directory='./files/')
server.listen()
