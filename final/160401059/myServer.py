import socket
from datetime import datetime , timedelta

#Berat Kanar 160401059

#2020-6-10 16:14:50  --> Date format.

#Zamanı gecikme ile birlikte hesapladığımız fonksiyon.
def getDate(ltncy):
    
    additionSeconds = str(ltncy)[5:7] #gecikme en fazla saniye cinsinden olacağından datetime cinsinden gelen gecikmeyi stringe çevirdik ve saniyeyi aldık.
    
    year = str(datetime.now().year)
    month = str(datetime.now().month)
    day = str(datetime.now().day)
    hour = str(datetime.now().hour)
    minute = str(datetime.now().minute)
    
    second = str(datetime.now().second)
    ExactSec=int(second)+int(additionSeconds)  #gecikmeyi ekledik ve gönderilecek zamanı bulduk.
    if(ExactSec<10):                        
        second='0'+str(ExactSec)
    else:
        second=ExactSec
    
    serverTime = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second
    

    return serverTime.encode()

#Gecikme hesaplamak için fonksiyon.
def getLtncy():
    t1 = datetime.utcnow() + timedelta(hours = utc) #İşleme başlamadan önceki zamanı alıyoruz.
    t2=str(t1)
    
    year = t2[:4] 
    t2 = t2[5:] 
    
    month = t2[:2] 
    t2 = t2[3:]
    
    day = t2[:2]
    t2 = t2[3:]
    
    t2 = year + '-' + month + '-' + day + ' ' + t2
    
    c.send(t2[:-3].encode('utf-8'))
    
    send= c.recv(1024)  #Veriyi yolluyoruz ve zamanı tekrar ölçerek arada verinin gidişi için gereken zamanı buluyoruz.
    zaman2 = datetime.utcnow() + timedelta(hours= utc)
    
    latency = (zaman2 - t1) / 2
    print(latency)
    return latency


host = "192.168.1.25"
port = 142
utc = 3



s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    
print("Server:Socket has been created..")
    
    
s.bind((host,port))
print("Socket connected to port {}".format(port))
    
s.listen(1)
print("Socket is listening...")
   


while True:
    
   c,addr = s.accept()
   
   late =getLtncy()  #gecikmeyi hesaplattık.
   
   x = getDate(late) #gecikmeyi de ekleyerek zamanı aldık.
   
   c.send(x)         # veriyi gönderdik.
   
   universalTimeC=str(utc)
   
   utcNew  = 'utc' + universalTimeC
   
   
   c.send(utcNew.encode())
   
   c.close()
   
   
    
