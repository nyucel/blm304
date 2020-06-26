import random 
import socket
import time
import struct
import sys

# HASAN SESLİ           # HASAN SESLİ
dosya = open("rota.txt", "w")
BUFFER_SIZE = 512

def rotaTakip(makinaAdi):
  
  try:
    hedef_ip = socket.gethostbyname(makinaAdi)

  except:
    print("\nMakina adini yanlis girdiniz yada hedef ip cözümlenemedi..\n")
    print("\nMakina adini dogru girerek tekrar deneyin..\n")
    sys.exit(1)

  maxRouter = 30
  ttl = 1
  portNumarasi = 33480

  proto_icmp = socket.getprotobyname('icmp')
  proto_udp = socket.getprotobyname('udp')

  
  print("%s icin traceroute kullaniyorsunuz ..\n" %makinaAdi)

  while True:
    aliciPaket = socket.socket(family=socket.AF_INET,type=socket.SOCK_RAW, proto=socket.IPPROTO_ICMP)
    zaman_asimi = struct.pack("ll", 999, 0)
    aliciPaket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, zaman_asimi)
    aliciPaket.bind(('', portNumarasi))

    gondericiPaket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    gondericiPaket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    gondericiPaket.sendto(b'', (hedef_ip, portNumarasi))

    adres = None #gelen adresi kontrol etmek icin degisken

    try:

      veri , adres = aliciPaket.recvfrom(BUFFER_SIZE)

    except socket.error as e:
      print(e)

    finally:
      aliciPaket.close()
      gondericiPaket.close()

    if adres:
      metin = "\n%s : tll ,  %s  : yonlendirici Adresi" %(ttl , adres[0])
      print(metin+"\n")
      dosya.write(metin + " \n")

      if (adres[0] == hedef_ip): # deger tekrar yönlendiriciye gelindiyse bitsin
        break

    else:
      metin = "%s :  * " %ttl
      print("%s :  * " %ttl)
      dosya.write(metin + "\n")

    ttl = ttl +1

    if (ttl > maxRouter):
      break

  dosya.close()


if __name__ == "__main__":

  if len(sys.argv) <= 1 :
    print("\nMakina adini yanlis yada eksik girdiniz.. tekrar acip tekrar deneyin\n")
    sys.exit(1)

  else:
    makinaAdi = sys.argv[1]
    rotaTakip(makinaAdi)
    
