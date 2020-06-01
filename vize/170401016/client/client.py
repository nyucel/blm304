# 170401016 - Can Sözbir
import socket
import os
import base64
import time
import random


def generate_random(n):
    return random.randrange(2**(n - 1), 2**n)


class Client:
    def __init__(self):
        self.ip = ''
        self.port = ''
        self.buffer_size = 1024
        self.address = ''
        self.client_socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_DGRAM
        )
        self.connected = False

    def set_ip(self, ip, port):
        self.ip = ip
        self.port = port
        self.address = (ip, port)

    def three_way_handshake(self, ip, port):
        seq = generate_random(32)
        self.client_socket.sendto(
            str(seq).encode(), (ip, port))

        response, address = self.client_socket.recvfrom(self.buffer_size)

        response = response.decode()

        server_ack, server_seq = response[:10], response[10:]

        ack = int(server_seq) + 1

        self.client_socket.sendto(
            (str(ack) + server_ack).encode(), (ip, port))

        self.set_ip(ip, port)
        return seq+1 == int(server_ack)

    def loop(self):
        self.client_socket.settimeout(3)

        while not self.connected:
            des_ip = input('Baglanti icin hedef ip giriniz: ')
            try:
                self.connected = self.three_way_handshake(des_ip, 42)
            except:
                print('baglanti saglanamadi... tekrar deneyin.')
        print('Baglandi basarili bir sekilde saglandi')

        while True:
            print(''' Komut seti
            ls              -> sunucuda tanimlanmis dizinde bulunan dosyalari listeler 
            put <dosyaadi>  -> sunucuya dosya yukler.
            get <dosyaadi>  -> sunucudan dosya indirir.
            ''')
            inp = input('komutunuzu giriniz: ')
            self.command(inp)

    def command(self, inp):
        if inp == 'ls':
            return(self.ls())

        else:
            splitted = inp.split(' ')
            if len(splitted) > 1:
                command = splitted[0]
                argument = ' '.join(splitted[1:])

                if command == 'put':
                    return(self.put(filename=argument))

                elif command == 'get':
                    return(self.get(filename=argument))
        print('Yanlis komut')

    def put(self, filename):
        if not os.path.exists(filename):
            print('Dosya bulunamadi.')
            return
        print(f'{filename} yukleniyor...')
        self.client_socket.settimeout(2)
        self.client_socket.sendto(
            ('put ' + filename).encode(), self.address)
        try:
            response = self.client_socket.recvfrom(
                self.buffer_size)
            print(response[0].decode())
        except:
            print('Baglanti hatasi.')
            return

        seq = generate_random(32)

        with open(filename, 'rb') as sendfile:
            data = sendfile.read(self.buffer_size-10)
            while data:

                self.client_socket.sendto(
                    str(seq).encode()+data, self.address)

                self.client_socket.settimeout(2)
                try:
                    received = self.client_socket.recvfrom(
                        self.buffer_size)
                    ack = int(received[0].decode())

                    if ack == seq + 1:
                        seq = ack
                        data = sendfile.read(self.buffer_size-10)

                except:
                    print(
                        'Dosya gonderilirken baglanti hatasi,',
                        'server.py ve client.py yi yeniden baslatip dosyayi tekrar gonderiniz ...')
                    self.connected = False
                    return
        self.client_socket.sendto(
            str(seq).encode()+b"<@EOF@>", self.address)

    def get(self, filename):
        self.client_socket.settimeout(2)
        self.client_socket.sendto(
            ('get ' + filename).encode(), self.address)
        try:
            response = self.client_socket.recvfrom(
                self.buffer_size)
            print(response[0].decode())
        except:
            print('Baglanti hatasi.')
            return

        with open(filename, 'wb+') as newfile:
            data, address = self.client_socket.recvfrom(
                self.buffer_size)
            while b"<@EOF@>" not in data:
                writedata = data[10:]
                newfile.write(writedata)

                seq = int(data[:10].decode())
                ack = seq + 1

                self.client_socket.sendto(str(ack).encode(), self.address)

                data, address = self.client_socket.recvfrom(
                    self.buffer_size)
        print(filename, f' dosyasi sunucudan yuklendi.')

    def ls(self):
        self.client_socket.settimeout(2)
        self.client_socket.sendto(
            ('ls').encode(), self.address)
        try:
            response = self.client_socket.recvfrom(
                self.buffer_size)
            print(response[0].decode())
        except:
            print('Baglanti hatasi.')
            return


client = Client()
client.loop()
