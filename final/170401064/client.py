# -*- coding: utf-8 -*-
import socket
import sys
import time
import datetime
import os
import argparse

if sys.platform == 'linux':
    if os.geteuid() != 0:
        exit("sudo ile çalıştırın")

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--server', help='Server Ip', nargs=1, type=str, required=True)
args = arg_parser.parse_args()

def _win_set_time(time_tuple):
    import pywin32
    dayOfWeek = datetime.datetime(time_tuple).isocalendar()[2]
    pywin32.SetSystemTime( time_tuple[:2] + (dayOfWeek,) + time_tuple[2:])


def _linux_set_time(time_tuple):
    import ctypes
    import ctypes.util
    import time

    CLOCK_REALTIME = 0

    class timespec(ctypes.Structure):
        _fields_ = [("tv_sec", ctypes.c_long),
                    ("tv_nsec", ctypes.c_long)]

    librt = ctypes.CDLL(ctypes.util.find_library("rt"))

    ts = timespec()
    ts.tv_sec = int( time.mktime( datetime.datetime( *time_tuple[:6]).timetuple() ) )
    ts.tv_nsec = time_tuple[6] * 1000000 # Millisecond to nanosecond
    librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))


start_time = time.time()

# TCP/IP socket oluşturuluyor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP adresi ve Port'u verilen server socket ile dinleniyor
server_address = (args.server[0], 142)
print('{}:{} bağlantı kuruluyor'.format(*server_address))
try:
    sock.connect(server_address)
except ConnectionRefusedError:
    exit("Bağlantı başarısız!")
except socket.gaierror:
    exit("Böyle bir sunucu bulunamadı")

try:
    # Veri gönderiliyor
    message = b'getmetime'
    #print('istek gönderiliyor {!r}'.format(message))
    sock.sendall(message)

    data = sock.recv(1024)
    #print('gelen veri {!r}'.format(data))

    server_time, server_zone = data.decode("utf-8").split(',')
    server_time = float(server_time)

    print("Milisaniye cinsinden zaman:", server_time, "\nZaman dilimi:", server_zone)

    stop_time = time.time()
    lateness = stop_time - start_time # İşlem sırasındaki gecikme hesaplanıyor

    current_time = server_time - lateness # Server süresinden gelen zaman verisininden gecikme miktarı çıkartılıyor
    time_extrication = time.localtime(current_time)
    
    time_tuple = (
        time_extrication.tm_year, # Year
        time_extrication.tm_mon, # Month
        time_extrication.tm_mday, # Day
        time_extrication.tm_hour, # Hour
        time_extrication.tm_min, # Minute
        time_extrication.tm_sec, # Second
        0, # Millisecond
    )

    if sys.platform == 'linux':
        _linux_set_time(time_tuple)
    elif  sys.platform == 'win32':
        _win_set_time(time_tuple)

    print("İşlem süresi: " + str(lateness) + " zaman sürdü")
finally:
    sock.close()
