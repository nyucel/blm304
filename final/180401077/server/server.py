#Ercan Berber 180401077

import socket
from datetime import datetime
from time import sleep
import threading


class server():
    def __init__(self):
        self.UTC = datetime.now().hour-datetime.utcnow().hour
        self.PORT = 142
        self.HOST = socket.gethostbyname(socket.gethostname()+".local")
        print(f"Serverın adresi..: {self.HOST}")
        
    def sv_init(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind((self.HOST,self.PORT))
        self.s.listen(1)

    def asd(self):
        print("Zaman dilimini değiştirmek için 3'e basın.")

        while True:
            if input()=="3":
                print(f"Şuanki zaman dilimi UTC {self.UTC}")
                print("Örnek giriş UTC-3 için -0300, UTC+3.5 için +0350")
                self.UTC = input("Yeni zaman dilimini girin.")
                self.UTC = float(self.UTC)/100


    def dinle(self):
        while True:
            self.connection, self.client_address = self.s.accept()
            print(self.client_address,"Bağlandı")
            self.gecikme=datetime.utcnow().timestamp()
            self.connection.send(str(self.gecikme).encode())
            self.gecikme=datetime.utcnow().timestamp()-float(self.connection.recv(1024))
            self.dt = (datetime.utcnow().timestamp()+self.gecikme+0.0002)*1000 
            self.dt += (self.UTC/1)*3600000 + (self.UTC%1)*60000 #3600000 saatin milisaniye, 60000 dakikanın milisaniye
            self.connection.send(str(self.dt).encode())
            sleep(0.0002)
            self.connection.send(str(self.UTC).encode())
            
    
    def threadler(self):
        x = threading.Thread(target=self.dinle)
        y = threading.Thread(target=self.asd)
        y.start()
        x.start()


sv = server()
sv.sv_init()
sv.threadler()
