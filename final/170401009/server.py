#!/usr/bin/env python
# -*- coding: utf-8 -*-
#1 second =1000 milliseconds
#time.time() fonksiyonu saniye cinsinden veriyor.

from scapy.all import * #sadece makine ip sini öğrenmek için kullanılıyor.
import socketserver
import pickle
import datetime
import time


class PaketHandler(socketserver.BaseRequestHandler):

    def handle(self):  # Override fonksiyon
        t1  = datetime.datetime.now() #CLIENTTEN PAKETIN GELDİĞİ ZAMAN
        self.timezone="UTC+2"         #TIMEZONE DEĞİŞTİRME YERİ
        veri = self.request.recv(1024)
        if veri.decode() == "TIME_REQUEST":

            print("{}:{} time request yaptı".format(self.client_address[0],self.client_address[1]))
            # data =  #milisaniye -> saniye
            self.request.send(pickle.dumps({"TIMEZONE":self.timezone,
                    "T1":t1 ,
                    "T2":datetime.datetime.now(), #SERVERDEN PAKETİN ÇIKTIĞI ZAMAN
                    "ZAMAN":time.time()*1000}))
        # print(threading.currentThread())
        return



if __name__ == '__main__':
    import threading

    bilgiler = (IP(dst='1.1.1.1').src, 127)  # let the kernel give us a port
    server = socketserver.TCPServer(bilgiler, PaketHandler)
    print("SERVER {}:{} Dinliyor".format(bilgiler[0],bilgiler[1]))
    t = threading.Thread(target=server.serve_forever) #çoklu kullanıcı ve arkada sürekli dinleme yapması için yaptım.
    t.setDaemon(False)                                # bunu yapmazsak program anında exit oluyor.
    t.start()

