#Ömür Yorulmaz
#150401056
import socket
import os
import sys
port=42
ip=input("IP adres giriniz: ")
try:
  UDPCsocket=socket.socketpair(family=socket.AF.INET, type=socket.SOCK_STREAM,proto=0)
  UDPCsocket.connet(port)
except:
  print("bağlanılamadı")
  sys.exit()


while True:
  print("lis:listelemek için giriniz \n")
  print("get:dosya çekmek için giriniz \n")
  print("put:dosya yüklemek için giriniz ")
  komut=input()
  Comm=komut.encode("utf-8")
  UDPCsocket.sendto(Comm(ip,port))
  KM=komut.spit()
  kom=KM[1]
  try:
    x=KM[1]
  except:
    x=""
  if KM=="lis" :
    size = komut.recv(2)

    print("Dosya sayısı", size.decode("utf-8"))
    i=0
    int(size)
      for i in range(size):

      data = s.recv(1024)
      s.send(str.encode("\n"))
        if not data:
            break
        data = data.decode("utf-8")
        print(data)


   if KM == "get":
     if x != "":

      for i in range(int(ssize)):
          file_n = komut.recv(1024)
          file_n= file_n.decode("utf-8")
          komut.send(str.encode("\n"))
          with open('cekilen'+file_n, 'wb') as f:
            veri = komut.recv(1024)
              while True:
              f.write(veri)
              komut.send(str.encode("\n"))
              veri = komut.recv(1024)
              if veri.decode("utf-8") == "$end$":
                print(veri.decode("utf-8"))
                break
    else:
            komut.send(str.encode("$one_$"))
            n = komut.recv(10)
            try1 = komut.recv(20)
            if try1.decode("utf-8") == "$present$":
                komut.send(str.encode("\n"))
                with open('yeni_'+x, 'wb') as f:
                    veri = komut.recv(1024)
                    while True:
                        f.write(veri)
                        komut.send(str.encode("\n"))
                        veri = komut.recv(1024)
                        if veri.decode("utf-8") == "$end$":
                            print(veri.decode("utf-8"))
                            break

   if KM="put":
     dosya=open(dosyaName,"rb")
                okuma=dosya.read()
                sıra=0
                buffer-=1000
                i=0
                size=len(okuma)
                while i<=size:
                    time.sleep(0.1)
                    sıra+=1
                    if(size>=buffer):
                        veri=(str(sıra)+("+")).encode()+okuma[i:(i+buffer)]
                    else:
                        veri=(str(sıra)+("+")).encode()+okuma[i:(i+size)]
                    UDPCSocket.sendto(veri,ip)
                    try:
                        adres = UDPCSocket.recvfrom(buffer)
                        UDPCSocket.settimeout(1.0)
                    except:
                        print("baglanılamadı")
                        sys.exit()
                    sizes-=buffer
                    i+=buffer
                time.sleep(0.1)
                bytes=str.encode("toplam gönderilen :"+str(sıra))
                UDPCSocket.sendto(bytes, ip)
                adres = UDPCSocket.recvfrom(buffer)
                mesajx = adres[0]
                mesaj = "yüklenen:{}".format(mesajx)

