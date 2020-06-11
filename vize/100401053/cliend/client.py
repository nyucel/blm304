import socket
from ftplib import FTP
import os
import sys ,time
from pathlib import Path

#Ahmet Orbay 100401053

serverAddress   = input("IP ADRES :  ")
serverAddressPort=(serverAddress,42)
bufferSize          = 4096
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.connect(serverAddressPort)

    
try:
    
    message="merhaba ben geldim"
    bytesToSend         = str.encode(message)
    clientIp= UDPClientSocket.getsockname()[0]
    UDPClientSocket.sendto(bytesToSend,serverAddressPort)


    try:
        UDPClientSocket.settimeout(5.0)
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg = "Message from Server {}".format(msgFromServer[0])
        
    except:
        print("baglanti saglanamadi")
        sys.exit()
    print(msg)

    islem=input("lutfen komutunuzu ve dosya ismini araya bir bosluk koyarak yaziniz yaziniz")
    dosyaName=islem[4::]

    message=islem[0:3]+" "+dosyaName
    bytesToSend         = str.encode(message)
    clientIp= UDPClientSocket.getsockname()[0]
    UDPClientSocket.sendto(bytesToSend,serverAddressPort)



    if(islem[0:3]!="put" and islem[0:3]!="get"):
                print("isteginiz uygun formatta degildir")
                exit()
            

    #GET

    if(islem[0:3].lower()=="get"):
                squenceNumber=0
                control=0
                dosya=open(dosyaName,"wb")
                while control==0:
                    try:
                        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
                        UDPClientSocket.settimeout(5.0)
                        msg = "{}".format(msgFromServer[0])
                    except:
                        print("Server ile baglanti kurulamadi")
                        sys.exit()
                    if(msg.find("son")<1):
                        dataParsing=msg.split("-")
                        mes=dataParsing[0]
                        message=mes[2::]
                        
                        squenceNumber+=1
                        data=dataParsing[1].split("'")
                        dosya.write(data[0].encode())
                        bytesToSend         = str.encode(message)
                        #clientIp= UDPClientSocket.getsockname()[0]
                        UDPClientSocket.sendto(bytesToSend,serverAddressPort)
                    elif (msg.find("son")>1):
                        finishControl=msg.split(":")
                        squenceServer=finishControl[1].split("'")
                        if(int(squenceServer[0])==squenceNumber):
                            bytesToSend         = str.encode("OK")
                            UDPClientSocket.sendto(bytesToSend,serverAddressPort)
                            print("isleminiz basari ile indirilmistir")
                            sys.exit()
                        else:
                            print("isleminiz gerceklesmemistir")
                            if( os.path.exists(dosyaName)):
                                os.remove(dosyaName)
                            sys.exit()
                        control=1
                    else:
                        if( os.path.exists(dosyaName)):
                            os.remove(dosyaName)
                        sys.exit()
                    
                sys.exit()


    #PUT
     
    if(islem[0:3].lower()=="put"):
                dosya=open(dosyaName,"rb")
                fileRead=dosya.read()
                sequenceNumber=0
                bufferSize-=100
                i=0
                sizes=len(fileRead)
                while i<=sizes:
                    time.sleep(0.2)
                    sequenceNumber+=1
                    if(sizes>=bufferSize):
                        data=(str(sequenceNumber)+("-")).encode()+fileRead[i:(i+bufferSize)]
                    else:
                        data=(str(sequenceNumber)+("-")).encode()+fileRead[i:(i+sizes)]
                    UDPClientSocket.sendto(data, serverAddressPort)
                    try:
                        bytesAddressPair = UDPClientSocket.recvfrom(bufferSize)
                        UDPClientSocket.settimeout(5.0)
                    except:
                        print("Server ile baglanti kurulamadi")
                        sys.exit()
                    sizes-=bufferSize
                    i+=bufferSize
                time.sleep(0.2)
                bytesToSend=str.encode("son toplam gonderim :"+str(sequenceNumber))
                UDPClientSocket.sendto(bytesToSend, serverAddressPort)
                bytesAddressPair = UDPClientSocket.recvfrom(bufferSize)
                message = bytesAddressPair[0]
                clientMsg = "Message from Server:{}".format(message)
                if(clientMsg.find("OK")>0):
                    print("isleminiz gerceklestirilmistir")
                    sys.exit()
                else:
                    print("Bir sorun olustu tekrar deneyiniz.")
                    sys.exit()

    
except socket.timeout:
    print("baglanti saglanamadi")
