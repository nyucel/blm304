import socket
import time
import datetime




host = "192.168.1.109"
port = 142

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket oluşturuldu")
    
    server.bind((host, port)) 
    print("socket {} nolu porta bağlandı".format(port))

    server.listen(5)      
    print("socket dinleniyor")
except socket.error as msg:
    print("Hata:",msg)

while True: 
   # Client ile bağlantı kurulursa 
   c, addr = server.accept()     
   print('Gelen bağlantı:', addr)
   mesaj = "[+][+] Merhaba Ben Server [+][+]"
   c.send(mesaj.encode())
   
   #zaman dilimi değiştirme
   utc = 2
   
   
   
   #zaman_dilim_degis(dilim_degis)
   utc = 3
   # Milisaniye cinsinden  Gönderilme 
   milisaniye = int(round(time.time()*1000))
   milisaniye = str(milisaniye)
   milisaniye = milisaniye + " utc+" + str(utc)
   c.send(milisaniye.encode())
   print(milisaniye)
   liste=[]
   liste = milisaniye.split()
   gelen_m = c.recv(1024).decode()
   
   son_m = int(round(time.time()*1000))
   
  
   #Gecikme Hesaplama
   gecikme = (int(liste[0]) - int(gelen_m)) // 2
   print(gecikme)
   gecikmeli = (son_m + gecikme) 
   gecikmeli =str(gecikmeli)
   c.send(gecikmeli.encode())
   
   
c.close()
