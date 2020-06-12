import socket
from datetime import datetime
import time

#Ahmet Orbay 100401053

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server=socket.gethostbyname(socket.gethostname())
server_address = (server, 142)
sock.bind(server_address)
sock.listen(1)

while True:
    timeZone="UTC +3"
    timeZonesign=timeZone[4:5]
    timeZoneHour=timeZone[5::]
    localZonesign=time.strftime('%Z%z')[20:21]
    localZoneHour=time.strftime('%Z%z')[21:23]
    if(timeZonesign=="-"):
        if(localZonesign=="+"):
            timeZoneFarki=-float(timeZoneHour)-float(localZoneHour)
        else:
            timeZoneFarki=-float(timeZoneHour)+float(localZoneHour)
    else:
        if(localZonesign=="+"):
            timeZoneFarki=float(timeZoneHour)-float(localZoneHour)
        else:
            timeZoneFarki=float(timeZoneHour)+float(localZoneHour)
    saatFarki=timeZoneFarki*3600000
    print ('waiting for a connection') 
    connection, client_address = sock.accept()
    try:
        print ('connection from', client_address)
        cevap =int(round(time.time() * 1000))
        response=str(cevap+saatFarki)+" UTC"+ timeZonesign+timeZoneHour
        connection.sendall(response.encode())
        print("response : ",response)
            
    finally:
        connection.close()