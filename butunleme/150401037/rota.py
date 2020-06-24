#150401037 HAKAN DURMAZ
import sys
import random
import socket
from scapy.all import *
from scapy.layers.inet import IP, UDP

hedef_adres = sys.argv[1]
hedef_ip = socket.gethostbyname(hedef_adres)                #Sunucunun adından dns sorgusu yapıyor.
print("Girdiginiz ip adresi: " +hedef_adres)
print("Girdiginiz adresin DNS sorgusu: "+hedef_ip)
f = open("rota.txt","w")

ttl_d=1                                                        #var olan ttl'i 1 olarak alıyor.
port = random.choice(range(1024, 65100))                     #Random port numarası alıyor.
for i in range(1, 31):
    paket = IP(dst=hedef_ip, ttl=ttl_d) / UDP(dport=port)
    rep = sr1(paket, verbose=0)
    f.write("\n*")
    if rep is None:
        print("* \n")

    elif rep.type == 3:
        print("", rep.src)
        break

    else:
        print('%s: %s' % (ttl_d, rep.src))

    ttl_d += 1
f.close()
