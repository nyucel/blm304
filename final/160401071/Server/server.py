#Arife Oran - 160401071

import socket
import time
import datetime


IP = '192.168.1.106'
Port = 142

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((IP, Port))
    print("IP: ", IP, " ", Port, ".port dinleniyor")
    serverSocket.listen(5)

except socket.error as message:
    print("Hata!", message)


conn,adrr = serverSocket.accept()
startTime = time.time()
print("Bağlantı kabul edildi")

msg = "Bağlantı Kuruldu"
conn.sendto(msg.encode(), (IP, Port))

def timeStamp():
    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)

temp= 1

while (temp):
    data = input("Zaman Dilimini Giriniz : UTC  ")
    if (data.startswith("+") or data.startswith("-") ):
        utc = int(data) -3
        timeStamp = timeStamp() +  int(utc) * 3600000
        sendTimeStamp = str(timeStamp) + '-UTC' + str(data)
        print(sendTimeStamp)
        conn.sendall(str(sendTimeStamp).encode('utf-8'))

        sTime = float(timeStamp) / 1000.0
        timeInfo = datetime.datetime.fromtimestamp(sTime).strftime('%m/%d/%Y %H:%M:%S.%f')
        print(timeInfo)
        temp=0

    else:
        print("Girdiğiniz zaman dilimi hatalıdır!")


serverSocket.close()