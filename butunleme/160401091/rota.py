# Veri Haberleşmesi Büt Ödevi
# Rabia Kaynak - 160401091

import sys
import os
from scapy.all import sr1, IP, ICMP

if len(sys.argv) != 2:
    sys.exit('Kullanım "sudo python3 rota.py www.comu.edu.tr" şeklinde olmalıdır.')

# TTL değeri 1 ile başlıyor ve arttırıyoruz.
ttl = 1

# Dosya yazma işlemini başlatıyoruz.
f = open('rota.txt', 'w')
f.write('Site: %s\n' % sys.argv[1])

print("Site: ", sys.argv[1])

i = 0
try:
    # 30 yönlendiriciye kadar deneme yapılmalıdır.
    for i in range (30):
        p = sr1(IP(dst=sys.argv[1], ttl=ttl) /
                ICMP(id=os.getpid()), verbose=0, retry=1, timeout=1)
        
        # Zaman aşımı
        # Tüm ICPM komutları için -> iana.org/assignments/icmp-parameters/icmp-parameters.xhtml
        if (p[ICMP].type == 11 and p[ICMP].code == 0):
            print('TTL: ', ttl, "- IP: ", p.src)
            f.write('TTL: %s - IP %s\n' % (ttl, p.src))
            ttl += 1
            i += 1

        elif (p[ICMP].type == 0):
            print('TTL: ', ttl, "- IP: ", p.src)
            f.write('TTL: %s - IP %s\n' % (ttl, p.src))
            i += 1
            break
except:
    pass
finally: 
    print("Dosya yazdırma tamamlandı.")
    f.close()
