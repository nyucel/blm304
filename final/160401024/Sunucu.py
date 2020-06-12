#-------------------SUNUCU------------------------
#160401024 Adem Çelik


import socket
import datetime


host = "127.0.0.1"
port = 142

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
   a = datetime.datetime.now()
   timenew= datetime.datetime.timestamp(a)

   # Bağlanan client tarafına hoşgeldin mesajı gönderelim.
   mesaj = str(timenew) + " UTC+3"
   c.send(mesaj.encode())
