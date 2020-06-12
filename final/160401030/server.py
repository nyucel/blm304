#160401030 - Yiğitcan ÜSTEK
import socket
import sys

import time


HOST = sys.argv.pop()
PORT = 142

var_time = "UTC+0"
sec = int(var_time[3:])
hour = sec* (3600*1000)

try:
    i = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST,PORT))
        server.listen(1)
        while True:
          print (server.getsockname(),' gelen bağlantı dinleniyor')
          sc, sockname = server.accept()
          print (sockname, " gelen bağlantı kabul edildi")
          print ('Soket ', sc.getsockname(), ' ve ', sc.getpeername(), ' bağlandı')
          
          while (i<100):
              sc.send("{0} {1}".format(time.time()+hour,var_time).encode('utf-8'))
              time.sleep(0.1)
              i+=1
          sc.recv(512)
          sc.send("{0} {1}".format(sec+time.time(),var_time).encode('utf-8'))
          print(sec+time.time())
        #sc.send(datetime.date.fromtimestamp(time.time()).ctime().encode('utf-8'))
        sc.close()    
except socket.error:
    print("Hata!")    



