import socket
import sys,os,time
from datetime import datetime

#Ahmet Orbay 100401053

def setComputerTime(totalTime):
    command=datetime.fromtimestamp(totalTime)
    os.system("sudo date --s  '%s'" % command)


def ConnectionServerTime(server,port):

    try:
        
        server_address = (server, int(port))
        print('connecting to %s port %s' % server_address)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
        sock.settimeout(5)
    except socket.error as error:
        print("baglanti saglanamadi",error)
        sys.exit()
    try:
        
        SendMessageTime=time.time()
        
        data = sock.recv(1024)
        timeSpent=(time.time()-SendMessageTime)*1000
        msSplit=(data.decode()).split(" ")
        ms=msSplit[0].split(".")
        totalTime=(float(ms[0])+float(timeSpent))/1000
        setComputerTime(totalTime)
        print("server response : ",data.decode())
        print("Converted Time : %s" %datetime.fromtimestamp(totalTime),msSplit[1])
    except socket.error as error:
        print(error)
    finally:
        sock.close()

if __name__ == '__main__':
    server=input("ip adresini giriniz : ")
    port=input("port numarasini giriniz : ")
    ConnectionServerTime(server,port)