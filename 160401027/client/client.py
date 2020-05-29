import socket
import pickle
import os
import sys

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
DESTINATION_UDP_PORT = 42
BUFFER_SIZE = 1024  # in bytes
CLIENT_EXAMPLE_FILES_FOLDER_NAME = "client_example_files/"
SERVER = ()


# Member variables
# Create UDP socket
sock = socket.socket(socket.AF_INET,  # AF_INET = IPv4
                     socket.SOCK_DGRAM)  # SOCK_DGRAM = UDP

did_connection_started = False
client_example_file_list = os.listdir(CLIENT_EXAMPLE_FILES_FOLDER_NAME)


def init():
    ip = str(input("Baglanmak istediginiz IP'yi giriniz(192.168.x.x): "))
    # ip = "192.168.86.130"
    initial_message = b"start_connection"

    global SERVER
    SERVER = (ip, DESTINATION_UDP_PORT)
    sock.sendto(initial_message, SERVER)


def get_client_example_files_as_string():
    global client_example_file_list
    client_example_file_list = os.listdir(CLIENT_EXAMPLE_FILES_FOLDER_NAME)
    result = ""
    for file in client_example_file_list:
        result += file + " "
    return result


def divide_file(buffer_size, filename, sequence_number):
    packet_list = list()
    sequence_number = format(sequence_number, "032b")
    with open(CLIENT_EXAMPLE_FILES_FOLDER_NAME + filename, "rb") as file:
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


def handle_data(data):
    # If data not empty
    if not not data:
        message_from_server = data.decode()
        if message_from_server.startswith("file_connection_start"):
            handle_incoming_file_transmission(message_from_server)
        else:
            print("[Server]: ", data.decode())


def handle_incoming_file_transmission(message_from_server):
    filename = message_from_server.split(" ")[1]

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
                print("[Client]: %s basariyla indirildi." % filename)
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


def handle_user_input(user_input):
    if user_input == "help":
        sock.sendto(user_input.encode(), SERVER)
    elif user_input.startswith("ls"):
        if user_input.split(" ")[1] == "local":
            print(get_client_example_files_as_string())
            sock.sendto(user_input.encode(), SERVER)
        elif user_input.split(" ")[1] == "server":
            sock.sendto(user_input.encode(), SERVER)
    elif user_input.startswith("put "):
        handle_outgoing_file_transmission(user_input)
    elif user_input.startswith("get "):
        sock.sendto(user_input.encode(), SERVER)


def handle_outgoing_file_transmission(user_input):
    requested_filename = user_input.replace("put ", "")
    global client_example_file_list
    client_example_file_list = os.listdir(CLIENT_EXAMPLE_FILES_FOLDER_NAME)
    if requested_filename in client_example_file_list:
        # File found
        message = ("file_connection_start " + requested_filename).encode()
        sock.sendto(message, address)

        file_packet_list = divide_file(BUFFER_SIZE, requested_filename, 0)

        for i in range(len(file_packet_list)):
            serialized_package = pickle.dumps(file_packet_list[i])
            sock.sendto(serialized_package, address)
        message = "file_connection_end".encode()
        sock.sendto(message, address)
    else:
        # File not found
        msg = b"not_found_in_client"
        sock.sendto(msg, address)


init()
while True:
    data, address = sock.recvfrom(BUFFER_SIZE)

    handle_data(data)

    # Tek seferlik(ilk baglantida)
    if did_connection_started == False and not not address:
        did_connection_started = True
        print("[Client]: Mümkün olan komutlari gormek icin 'help' yaziniz...")

    user_input = str(input("user~: "))
    handle_user_input(user_input)
