import socket
import os


class Client:
    def __init__(self, hedef_host):
        self.hedef_host = hedef_host  # hedef server'in ip si
        self.hedef_port = 142
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer_size = 256

    def connect(self):
        self.client_socket.connect((self.hedef_host, self.hedef_port))

    def send_package_delay(self):
        message = self.client_socket.recv(self.buffer_size)
        self.client_socket.send(message)

    def listen(self):
        self.connect()

        while True:
            inp = input(
                'Baglantiyi iki tarafli sonlandirmak icin Q, saatinizi guncellemek icin S giriniz: ')

            if inp == 'Q':
                self.client_socket.send(inp.encode())
                self.client_socket.close()
                break
            elif inp == 'S':
                self.client_socket.send(inp.encode())
                self.send_package_delay()
                time_from_server = self.client_socket.recv(self.buffer_size)
                time_from_server = time_from_server.decode()

                time, utc = time_from_server.split('[@]')
                print(utc)
                print(
                    f'Saat ve tarihiniz {utc} olacak sekilde {time} ile guncellenecek...')
                try:
                    linux_change_time_command = f'date --set="{time}"'
                    os.system(linux_change_time_command)
                    os.system("sudo hwclock -w")

                except:
                    print('Saat guncellenirken bir hata olustur. ')


hedef_ip = input('Baglanacaginiz sunucunun ip adresini giriniz: ')
client = Client(hedef_host=hedef_ip)
client.listen()
