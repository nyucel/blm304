from scapy.all import *
import socket
import time
import os
import sys

#Furkan Soysal 160401017
_sport=70
_dport=70
_src=socket.gethostbyname(socket.gethostname())
path=os.getcwd()

def send_packetWithAction(action,data,_dstHost):
    spacket=IP(dst=_dstHost)/UDP(sport=_sport,dport=_dport)/Raw(load=str(data))/Padding(load=action)
    send(spacket)
def listen_packet():
    return sniff(filter="udp port 70",count=1)

if len(sys.argv) != 2:
    print("İki argüman ile çalışmaktadır.Bağlanılacak bir host bilgisi girmelisiniz.")
    sys.exit()


_dstHost=sys.argv[1]
print(_dstHost)

while True:

    command = input(
        "Aşağıdaki komutlardan birini giriniz: \n1. get [dosya ismi]\n2. put [dosya ismi]\n3. list\n4. exit\n ")

    """o get [dosya ismi]
    o put [dosya ismi]
    o list
    o exit"""
    if len(command)>3:

        clientArguments = command.split()
        if clientArguments[0]=='exit':
            send_packetWithAction(clientArguments[0],str("exit").encode('utf-8'),_dstHost)
            break
        elif clientArguments[0]=='list':
            send_packetWithAction(clientArguments[0],str("list").encode('utf-8'),_dstHost)
        elif clientArguments[0]=='get':
            send_packetWithAction(clientArguments[0],clientArguments[1],_dstHost)
        elif clientArguments[0] == "put":
            print("Client put başlatılıyor")
            path=path+"\\"+clientArguments[1]
            if os.path.isfile(path):
                print("Seçilen dosya clientte mevcut upload başlıyor.")
                sending_file=open(path,'r')
                Runs=sending_file.read()
                sending_file.close()
                send_packetWithAction("upload"+clientArguments[1],Runs,_dstHost)

        lpacket=listen_packet()
        # print(lpacket[0].load.decode())

        # print(lpacket[0][Padding].load.decode())

        data=lpacket[0].load.decode()#Raw decode

        packet_command=lpacket[0][Padding].load.decode() #Padding decode
            
        if packet_command=='received':
            print("\nClient get başlatılıyor.\n")
            ComingFile = open(clientArguments[1], "w")
            ComingFile.write(data)
            ComingFile.close()
            print("\nDosya Başarılı indirildi.\n")
        
        elif packet_command=='listed':
            print("\nServer'daki dosyalar.\n",data,"\n")

quit()                