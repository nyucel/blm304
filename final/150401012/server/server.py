#Yiğit Yüre 150401012

import socket
import datetime

HOST = "192.168.0.1"
PORT = 142

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

while True:
    conn, addr = s.accept()
    print 'Bağlantı kuruldu ', addr
    while True:
        try:
            firsttime = str(datetime.datetime.utcnow())
            data = conn.recv(1024)
            wish = input("UTC değeri +3'tür, değiştirmek iste misiniz? /e,h: ")
            
            if(wish == "e"):
                utc = str(input(" UTC değerini belirtin (+3,-2..): "))
                utc1 = int(utc) - 3
                secondtime = datetime.datetime.now()
                difference = secondtime - firsttime
                time = secondtime + difference
                time1 = time + datetime.timedelta(hours = utc1)
                (time2, micro) = time1.strftime('%Y-%m-%d %H:%M:%S.%f').split('.')
                time2 = "%s.%03d" % (time2, int(micro) / 1000)
                realtime = time2 + " UTC" + utc
            if (wish == "h"):
                secondtime = str(datetime.datetime.utcnow())
                difference = secondtime - firsttime
                time = secondtime + difference
                (time2, micro) = time.strftime('%Y-%m-%d %H:%M:%S.%f').split('.')
                time2 = "%s.%03d" % (time2, int(micro) / 1000)
                realtime = time2 + " UTC+3"

            conn.sendall(realtime.encode())
        except socket.error, msg:
            print 'Sunucu ile bağlanrı kurulamadı ', addr
            break
    conn.close()