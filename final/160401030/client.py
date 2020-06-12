#160401030 - Yiğitcan ÜSTEK
import socket, sys
import os,time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)




HOST = sys.argv.pop() if len(sys.argv) == 3 else '127.0.0.1'
PORT = 142

ar = []

i = 0

s.connect((HOST, PORT))
print ("{0}".format(s.getsockname()) + " bağlanıldı")
    
while(i<100):
    ar.append(s.recv(1024).decode('utf-8').split(" ")[0])
    
    i+=1


for i in range(len(ar)):
    ar[i] = float(ar[i])
toplam = 0
for i in range(len(ar)-1):
    toplam += ar[i+1]-ar[i] 

toplam = toplam / len(ar)
print("Ortalama Gecikme süresi:%s" % toplam)
s.send("1".encode('utf-8'))



msg = s.recv(1024).decode('utf-8')
print(msg)
saat = float(msg.split(" ")[0]) + toplam

try:
    os.system('sudo date --set="'+time.ctime(saat)+'"')
    print("Tarih " + time.ctime(saat) + " olarak ayarlandı!"  )
except:
    print("Bilgisayarın saati ayarlanamadı!")

s.close()

