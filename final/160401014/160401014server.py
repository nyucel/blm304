#Selin KURT 160401014
import socket
import time
import datetime

newsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('0.0.0.0', 142)
print('{} port {}'.format(*server_address))
newsocket.bind(server_address)
newsocket.listen(5)

while 1:
    print("sunucu bekliyor")
    
    info, istemci_ip = newsocket.accept()
    print('istemci ip:', istemci_ip)
    
    data = info.recv(1024)
    time1 = datetime.datetime.utcnow()  
    time2 = datetime.datetime.now()   
    utc_time = time2-time1

    UTC = "UTC" + str(utc_time)[0]
    time_now = int(round(time.time()*1000))
    info.send(str(time_now).encode())
    info.close()
