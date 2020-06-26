# Şamil GÜVEN 160401038

import sys
import socket
import random
import struct
import os

if os.geteuid() != 0:
    exit("script root hakları ile çalıştırılmalıdır.")
dest_name = sys.argv[1]
hedefIP = socket.gethostbyname(dest_name)


maxTTL = 30


file = open("rota.txt", "w")

for ttl in range(1, maxTTL+1):
    for i in range(3):
        try:
            listen = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            timeout = struct.pack("ll", 2, 0)
            listen.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)
            listen.bind(('', 0))
            udpsend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            udpsend.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
            udpsend.sendto(b'data', (hedefIP, random.choice(range(33434, 33535))))
            _, gecerliIP = listen.recvfrom(512)
            gecerliIP = gecerliIP[0]
            print("TTL",ttl,": ",gecerliIP)
            file.write("{}\n".format(gecerliIP))
            break
        except socket.error:
             print("TTL",ttl,": Tekrar deneniyor", i)
             pass
        finally:
            listen.close()
            udpsend.close()

    if gecerliIP == hedefIP:
        break

file.close()
print("Yönlendirici ip adresleri dosyaya yazdırıldı.")