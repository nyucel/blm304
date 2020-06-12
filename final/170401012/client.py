
#Beyza ÇOBAN
#170401012

from socket import*
from os import system, name
import os
import time
import sys
from datetime import datetime
import socket


IP=input("\nBaglanılacak Sunucu IP: ")
PORT= 142

utc_bilgisi = open("utc.txt", "r")
utc = utc_bilgisi.read()
utc_bilgisi.close()
        
print("\n Sunucudaki zaman dilimi : ", utc)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as istemci:
        istemci.connect((IP, PORT))
        istemci.send(bytes("gecikmesüresi", encoding='utf-8'))

        kontrol = istemci.recv(1024)
        print("\n Kontrol için gönderilen zaman alındı\n")

        istemci.send(bytes("test", encoding='utf-8'))
        yeni_zaman = istemci.recv(1024)
        
      
        print("\n Sistemin güncellenmesi gereken zaman :", yeni_zaman.decode("utf-8"))
        
        
        os.system('date --set "%s" +\"%%A %%d %%B %%Y %%H:%%M:%%S.%%6N\"' % yeni_zaman.decode("utf-8"))
        print("\nSistem saati başarıyla güncellendi\n")
        istemci.close()

if __name__=="__main__":
    main()
