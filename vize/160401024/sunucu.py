
#-------------------SUNUCU------------------------
#160401024 Adem Çelik


import socket
import sys
import select
import threading



def putt(filename):
    global s
    datas = c.recv(1024)
    f = open(filename, "wb")
    while datas:
        f.write(datas)
        datas = c.recv(1024)
    f.close()
    print("{} alındı...".filename)

def gett(filename):
    global s
    dosya = open(filename, "rb")
    dosya2 = dosya.read()
    print(type(dosya2))
    print(len(dosya2))
    dosya.close()
    s.sendall(dosya2)

def listele():
    global s
    dosyalar=open("dosyalar.txt","w")
    for i in dosyalistesi():
        dosyalar.write(i)

    dosyalar.close()


host="127.0.0.1"
port=42

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket oluşturuldu")

    s.bind((host, port))
    print("socket {} nolu porta bağlandı".format(port))

    s.listen(5)
    print("socket dinleniyor")
except socket.error as msg:
    print("Hata:",msg)

while True:

   # Client ile bağlantı kurulursa
   c, addr = s.accept()
   print('Gelen bağlantı:', addr)

   # Bağlanan client tarafına hoşgeldin mesajı gönderelim.
   mesaj = 'Bağlantı yapıldı...'
   c.send(mesaj.encode('utf-8'))
   while True:
       s.recv(str.encode(komut))
       komut_ayir = komut.split(" ")
       cm = komut_ayir[0]

       try:
           filename = komut_ayir[1]
       except:
           filename = ""

       if (cm == "get"):
           gett()

       elif (cm == "put"):
           putt()
       elif (cm == "ls"):
           listele()
       else:
           print()
           s.close()

