import socket
import pickle
import platform
import datetime
import subprocess
import os

# 170401028 - Emir Kıvrak

class Client:
    def __init__(self, server_ip="192.168.0.100", server_port=127):
        self.SERVER_IP = server_ip
        self.SERVER_PORT = server_port
        self.CLIENT_SOCKET = self.init_socket_and_connect_server()


    def init_socket_and_connect_server(self):
        """Client socketi kur ve servere bağlantı isteği yolla"""
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client.connect((self.SERVER_IP, self.SERVER_PORT))
        return tcp_client

    def send_msg_and_listen(self, msg):
        """Servere bir mesaj yolla ve yanıtı döndür"""

        self.CLIENT_SOCKET.sendall(msg.encode())
        print("Bytes Sent:     {}".format(msg))

        received = self.CLIENT_SOCKET.recv(1024)
        received = pickle.loads(received)
        print("Bytes Received: {}".format(received))
        return received




    def miliseconds_to_datetime_object(self, millis):
        """
        milisecond -> datetime object
        """
        seconds = millis / 1000.0
        time = datetime.datetime.fromtimestamp(seconds)  ## şu an zaman datetime objesine dönüştü

        return time

    def SET_CLOCK(self):
        """
        Önce clientin hangi işletim sistemi üzerinde koştuğunu anlayıp,
        ona göre işlem yapacağız.

        """

        T0 = datetime.datetime.now() # zaman damgası (timestamp) -0-

        request = self.send_msg_and_listen("TIMEREQUEST")  # sunucuya zamanı öğrenmek için bir istekte bulunuyoruz.
        milliseconds = request["TIME"]  # request TIMEZONE ve milisaniye cinsinden zamanı tutuyor şu an.

        #t2 ve t3 zamanları sunucudan yollanıyor
        T1 = request["T1"]
        T2 = request["T2"]

        time = self.miliseconds_to_datetime_object(milliseconds)
        plt = platform.system()

        T3 = datetime.datetime.now()

        round_trip_delay = (T3-T0) - (T2-T1) # gidiş geliş gecikmesi 
        #offset =  ((T1-T0) + (T3-T2)) / 2 -ofset değerini böyle hesaplanıyor, ama bunu kullanmayacağım, belki sonra bununla da uğraşırım.
        print("Round trip delay : " + str(round_trip_delay))
        #print("Offset : " + str(offset))
        if plt == "Linux":
            newdate = subprocess.Popen(["sudo", "date", "-s", str((time+round_trip_delay))])
            newdate.communicate()
            print("Saat güncellendi")

        else:
            print("Linux harici bir işletim sisteminde çalıştırıldı, çıkılıyor.")
            exit(1)

input_ip = input("Lütfen sunucunun ip adresini giriniz")
c = Client(server_ip = input_ip)
c.SET_CLOCK()
