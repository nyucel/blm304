import socket
import os
import sys
import pickle

# Göksu Türker
class Packet:
    def __init__(self, sequence_number, data_in_bytes, eof=False):
        self.sequence_number = sequence_number
        self.data_in_bytes = data_in_bytes
        self.eof = eof

    def print_packet(self):
        print('Sequence Number: ', self.sequence_number)
        print('End of File: ', self.eof)


# Constants
SERVER_UDP_PORT = 42
BUFFER_SIZE = 1024  # in bytes
SERVER_EXAMPLE_FILES_FOLDER_NAME = "server_example_files/"


# Member variables
sock = socket.socket(socket.AF_INET,  # AF_INET = IPv4
                     socket.SOCK_DGRAM)  # SOCK_DGRAM = UDP

did_connection_started = False
server_example_file_list = os.listdir(SERVER_EXAMPLE_FILES_FOLDER_NAME)


def init():
    ip = str(input("Sunucu makinenin IPv4 adresini giriniz(192.168.x.x): "))
    # ip = "192.168.86.130"
    sock.bind((ip, SERVER_UDP_PORT))
    print("...UDP ile server baslatildi ve dinlemeye basladi...")


def handle_data(data):
    # If data not empty
    if not not data:
        message_from_client = data.decode()
        print("Kullanicidan %s mesaji geldi." % message_from_client)
        if message_from_client == "start_connection":
            global did_connection_started
            did_connection_started = True
            print("%s:%s sunucuya baglandi. Cevap gönderiliyor..." % (address[0], address[1]))
            message = b"UDP baglantisi basariyla kuruldu!"
            sock.sendto(message, address)
        elif message_from_client == "help":
            message = "Mümkün olan komutlar:\n" \
                      "'help' komutu ile mümkün olan komutlari görebilirsiniz.\n" \
                      "'ls local' komutu ile istemcideki dosyalari görebilirsiniz.\n" \
                      "'ls server' komutu ile sunucudaki dosyalari görebilirsiniz.\n" \
                      "'put [filename]' komutu ile sunucuya dosya yükleyebilirsiniz.\n" \
                      "'get [filename] ile sunucudan dosya indirebilirsiniz.'".encode()
            sock.sendto(message, address)
        elif message_from_client == "ls local":
            msg = b"Sunucuya dosya upload etmek icin put komutunu kullanabilirsiniz."
            sock.sendto(msg, address)
        elif message_from_client == "ls server":
            msg = get_server_example_files_as_string().encode()
            sock.sendto(msg, address)
        elif message_from_client.startswith("file_connection_start "):
            handle_incoming_file_transmission(message_from_client)
        elif message_from_client.startswith("get "):
            handle_outgoing_file_transmission(message_from_client)
        elif message_from_client == "not_found_in_client":
            msg = "İstemcide bulunmayan bir dosyayi upload etmeye calistiniz tekrar deneyin...".encode()
            sock.sendto(msg, address)
        else:
            print("Kullanici yanlis bir komut girdi.(komut: %s)" % message_from_client)
            msg = "Beklenmedik bir komut girdiniz.".encode()
            sock.sendto(msg, address)


def handle_incoming_file_transmission(message_from_client):
    filename = message_from_client.split(" ")[1]

    byte_list = list()
    while True:
        data_chunk = sock.recvfrom(BUFFER_SIZE * 2)[0]
        try:
            message = data_chunk.decode()
            # Sunucudan file_connection_end mesajı gelene kadar data_chunk degiskenini decode
            # etmek hata veriyor. Bu yüzden except blogu ile fonksiyonu devam ettiriyorum.
            # Sunucu 'file_connection_end' mesajını gönderdikten sonra decode islemi hata
            # vermiyor ve if bloguna girip while blogundan cikiyor.
            if message == "file_connection_end":
                msg = b"Dosyayi basariyla upload ettiniz."
                sock.sendto(msg, address)
                break
        except:
            pass

        # De-serialize Packet object
        packet = pickle.loads(data_chunk)
        byte_list.append(packet.data_in_bytes)

    # file_connection_end mesajı geldikten sonra byte_list'te bulunan byte degerlerini
    # dosyaya yazdiriyorum
    with open(filename, "wb") as f:
        for i in range(len(byte_list)):
            f.seek(i * BUFFER_SIZE)
            arr = bytearray(byte_list[i])
            f.write(arr)
    f.close()


def get_server_example_files_as_string():
    global server_example_file_list
    server_example_file_list = os.listdir(SERVER_EXAMPLE_FILES_FOLDER_NAME)
    result = ""
    for file in server_example_file_list:
        result += file + " "
    return result


def handle_outgoing_file_transmission(message_from_client):
    requested_filename = message_from_client.replace("get ", "")
    global server_example_file_list
    server_example_file_list = os.listdir(SERVER_EXAMPLE_FILES_FOLDER_NAME)
    if requested_filename in server_example_file_list:
        # File found
        message = ("file_connection_start " + requested_filename).encode()
        sock.sendto(message, address)

        file_packet_list = divide_file(BUFFER_SIZE, requested_filename, 0)
        for i in range(len(file_packet_list)):
            serialized_package = pickle.dumps(file_packet_list[i])
            sock.sendto(serialized_package, address)
        message = b"file_connection_end"
        sock.sendto(message, address)
    else:
        # File not found
        msg = "%s adli dosyayi bulamadim :(" % requested_filename
        sock.sendto(msg.encode(), address)


def divide_file(buffer_size, filename, sequence_number):
    packet_list = list()
    sequence_number = format(sequence_number, "032b")
    with open("server_example_files/"+filename, "rb") as file:
        binary_data = file.read()
        i = 0
        length = sys.getsizeof(binary_data)
        while i <= length:
            file.seek(i)
            chunk_data = file.read(buffer_size)
            if i + buffer_size > length:
                packet_list.append(Packet(sequence_number, chunk_data, True))
            else:
                packet_list.append(Packet(sequence_number, chunk_data, False))
            i += buffer_size
            t = int(sequence_number, 2) + 1
            sequence_number = format(t, "032b")
    return packet_list


init()
while True:
    data, address = sock.recvfrom(BUFFER_SIZE)

    handle_data(data)
