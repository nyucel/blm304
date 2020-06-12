import socket
import time
import pickle


# Sunucu bilgisayarının sahip oldugu zaman dilimini return eder
def get_current_system_utc_offset():
    offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone

    utc_offset = int(offset / -3600)
    return utc_offset

# 160401027 - Göksu Türker
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-* YAPILANDIRMA YAPILACAK KISIM -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

# Eger sunucu yaziliminin zaman diliminde sistemin zaman dilimi degil de ozel bir zaman dilimi kullanmak istiyorsaniz,
# UTC_OFFSET degiskenine tam sayı(-7, +3, ex...) atayarak yapabilirsiniz.
# Eger sunucu yaziliminin zaman dilimi icin tekrar sistemin zaman dilimini kullanmak istiyorsaniz,
# UTC_OFFSET degiskenine get_current_system_utc_offset() atayabilirsiniz
UTC_OFFSET = get_current_system_utc_offset()

# Sunucu bilgisayarının IP'sini buradan degistirebilirsiniz.
IP = "192.168.86.132"

# *-*-*-*-*-*-*-*-*-*-*-*-*-*-* YAPILANDIRMA YAPILACAK KISIM -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*


class TimeMessage:
    def __init__(self, time_in_millis, utcoffset):
        self.time_in_millis = time_in_millis
        self.utcoffset = utcoffset


# Constants
TCP_PORT = 142

# Member variables
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def init():
    sock.bind((IP, TCP_PORT))
    sock.listen(1)
    print("...Şu anda sunucu bilgisayarının zaman dilimi: UTC ", get_current_system_utc_offset())
    print("...Sunucu yazılımının zaman dilimi ise: UTC ", UTC_OFFSET)
    print("...İstemcilere gönderilecek zaman dilimini UTC_OFFSET adlı degiskene tam sayı degeri vererek degistirebilirsiniz...")
    print("...TCP server baslatildi ve dinlemeye basladi...")


def current_time_in_millis():
    return int(time.time() * 1000)


def send_time_message_to_client(connection):
    message = TimeMessage(current_time_in_millis(), UTC_OFFSET)
    print("Sending data to client: %sms, UTC %s" % (message.time_in_millis, message.utcoffset))
    serialized_package = pickle.dumps(message)
    connection.send(serialized_package)


init()
while True:
    # accept incoming connections and print
    connection, address = sock.accept()
    print("Client: ", connection.getpeername())

    # get data from accepted connection
    data = connection.recv(512)

    # if data not empty
    if not not data:
        send_time_message_to_client(connection)
