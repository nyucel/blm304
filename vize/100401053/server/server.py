import socket
import os
from ftplib import FTP
from scapy.all import *

#Ahmet Orbay 100401053

localIP     = socket.gethostbyname(socket.gethostname())
localPort   = 42
bufferSize  = 4096
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
UDPServerSocket.bind((localIP, localPort))
    
try:
    
    print("UDP server up and listening") 
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    control=1
    fileNames=":"
    dosyaPath=os.getcwd()
    os.chdir(dosyaPath+"/serverfilelist")
    for i in os.listdir():
        fileNames=fileNames+" , "+i
    if(clientMsg != ""):
        bytesToSend=str.encode("Hosgeldiniz baglantiniz kurulmustur. islem yapabileceginiz dosyalar "+fileNames)
        UDPServerSocket.sendto(bytesToSend, address)
        

    
    
    while(control==1):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

        message = bytesAddressPair[0]

        address = bytesAddressPair[1]

        clientMsg = "Message from Client:{}".format(message)
        messageC=message.decode()
        messageSplit=messageC.split("'")


        
        if((messageC[0:3].lower())=="get"):
            dosyaName=messageC[4::]
            dosya=open(dosyaPath+"/serverfilelist/"+dosyaName,'rb')
            a=dosya.read()
            i=0
            bufferSize-=100
            sequenceNumber=0
            sizes=len(a)
            while i<=sizes:
                time.sleep(0.2)
                sequenceNumber+=1
                if(sizes>=bufferSize):
                    data=(str(sequenceNumber)+("-")).encode()+a[i:(i+bufferSize)]
                else:
                    data=(str(sequenceNumber)+("-")).encode()+a[i:(i+sizes)]
                UDPServerSocket.sendto(data, address)
                bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
                sizes-=bufferSize
                i+=bufferSize
                message = bytesAddressPair[0]
            time.sleep(0.2)
            bytesToSend=str.encode("son toplam gonderim :"+str(sequenceNumber))
            UDPServerSocket.sendto(bytesToSend, address)
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

            message = bytesAddressPair[0]
            clientMsg = "Message from Client:{}".format(message)
            if(clientMsg.find("OK")>0):
                print(clientMsg)
                sys.exit()


        if((messageC[0:3].lower())=="put"):
            squenceNumber=0
            control=0
            dosyaName=messageC[4::]
            dosya=open(dosyaPath+"/serverfilelist/"+dosyaName,"wb")
            while control==0:
                msgFromServer = UDPServerSocket.recvfrom(bufferSize)
                msg = "{}".format(msgFromServer[0])
                if(msg.find("son")<1):
                    dataParsing=msg.split("-")
                    mes=dataParsing[0]
                    message=mes[2::]
                    
                    squenceNumber+=1
                    data=dataParsing[1].split("'")

                    dosya.write(data[0].encode())
                    bytesToSend         = str.encode(message)
                    UDPServerSocket.sendto(bytesToSend,address)
                else:
                    finishControl=msg.split(":")
                    squenceServer=finishControl[1].split("'")
                    if(int(squenceServer[0])==squenceNumber):
                        bytesToSend         = str.encode("OK")
                        UDPServerSocket.sendto(bytesToSend,address)
                        print("islem basari ile gerceklestirilmistir")
                    else:
                        print("isleminiz gerceklesmemistir")
                        os.remove(dosyaName)
                    control=1
                
            sys.exit()
        sys.exit()
        
        
except(KeyboardInterrupt, SystemExit):
    raise