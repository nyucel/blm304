from scapy.all import *
import socket
import time
import os
import sys

#Furkan Soysal 160401017
# _iface="Intel(R) Dual Band Wireless-AC 8260"
_srcHost=socket.gethostbyname(socket.gethostname())
_sport=42
_dport=42

def send_packetWithAction(action,data,_dstHost):
    spacket=IP(dst=_dstHost)/UDP(sport=_sport,dport=_dport)/Raw(load=str(data))/Padding(load=action)
    send(spacket)


def GETFILE(filename):
    path=os.getcwd()+"\\files\\"+filename
    print("getin iindeyim")
    if os.path.isfile(path):
        print("\nDosya Server'da bulunmakta. Devam ediliyor.\n")
        SendingFile = open(path, "r")
        RunS = SendingFile.read()
        # print(RunS)
        SendingFile.close()
        send_packetWithAction("received",RunS,_dstHost)
    else:
        print("Aranan dosya server'da yok.")
def PUTFILE(filename,data):
    path=os.getcwd()+"\\"+filename
    if os.path.isfile(path):
        print("Server'da {filename} isimli dosya mevcut değildir..Tekrar deneyiniz.")
    else:
        print("\nServer'a yazma başlıyor.\n")
        savedFile = open(path, "w")
        dataS = savedFile.write(data)
        savedFile.close()
        print("\nServer'a yazma bitti.\n")
def LIST():
    path=os.getcwd()+"\\files"
    Files = os.listdir(path)
    print(Files)
    return Files

while True:
    rpacket=sniff(filter="udp port 70",count=1)
    print("Yakalanan paket büyüklüğü:",rpacket.count)
    data=rpacket[0].load.decode() #Raw decode
    packet_command=rpacket[0][Padding].load.decode() #Padding decode
    _dstHost=rpacket[0][IP].src
    if len(str(packet_command))>=3:

        if str(packet_command).startswith('upload'):
            filename=str(packet_command)
            filename=str(filename).replace('upload','')
            packet_command='upload'
            # print(filename)
            
        

        # print(data)
        # print("Yollanan istek",packet_command)
        if packet_command=="get":
            print("Server get çağırıldı.")
            GETFILE(data)
        elif packet_command=="upload":
            print("Upload başlatılıyor.")
            print(filename)
            PUTFILE(filename,data)
        elif packet_command == "list":
            print("list çağırıldı.")
            Files=LIST()
            send_packetWithAction("listed",Files,_dstHost)
        elif packet_command == "exit":
            print("Server kapatılıyor.")
            break
    else:
        print("Paket'te komut bulunamadı bulunamadı....") 

quit()