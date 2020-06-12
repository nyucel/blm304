import socket
import pickle
import datetime
import subprocess
import shlex
# 160401027 - Göksu Türker
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-* YAPILANDIRMA YAPILACAK KISIM -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

# İstemcinin baglanacagi IP adresini buradan degistirebilirsiniz.
IP = "192.168.86.132"

# *-*-*-*-*-*-*-*-*-*-*-*-*-*-* YAPILANDIRMA YAPILACAK KISIM -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*


class TimeMessage:
    def __init__(self, time_in_millis, utcoffset):
        self.time_in_millis = time_in_millis
        self.timezone = utcoffset


# Member variables
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

initial_message = b"give_me_time"

# Connect to server and request time
DESTINATION_TCP_PORT = 142
SERVER = (IP, DESTINATION_TCP_PORT)
sock.connect(SERVER)
sock.sendall(initial_message)

# Get time data from server
data = sock.recv(512)
TIME_MESSAGE = pickle.loads(data)

# Get UTC+00 date from TIME_MESSAGE.time_in_millis
date = datetime.datetime.fromtimestamp(TIME_MESSAGE.time_in_millis / 1000.0)

# Add utcoffset to date
date = date + datetime.timedelta(hours=TIME_MESSAGE.utcoffset)

date_tuple = (
    date.year,
    date.month,
    date.day,
    date.hour,
    date.minute,
    date.second,
    date.microsecond
)

date_string_for_command = datetime.datetime(*date_tuple).isoformat()

# disable network time protocol
subprocess.call(shlex.split("timedatectl set-ntp false"))

# set system's date with date_string
subprocess.call(shlex.split("sudo date -s '%s'" % date_string_for_command))
subprocess.call(shlex.split("sudo hwclock -w"))
