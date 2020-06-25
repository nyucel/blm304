#ZELİHA DÖNER 160401004
import random 
import socket
import time
import struct
import sys

class Tracer(object):
    def __init__(self,dst,hops=30):
        self.dst=dst
        self.hops=hops
        self.ttl=1
        self.port=random.choice(range(33434, 33535))

    #alıcı soketi oluşturma
    def alici_f(self):
        s = socket.socket(family=socket.AF_INET,type=socket.SOCK_RAW,proto=socket.IPPROTO_ICMP)
        timeout = struct.pack("ll", 5, 0)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)
        s.bind(('', self.port))
        return s

    #gönderen soketi oluşturma
    def gonderici_f(self):
        s = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM,proto=socket.IPPROTO_UDP)
        s.setsockopt(socket.SOL_IP, socket.IP_TTL, self.ttl)
        return s

    #tracer i çalıştırmak için
    def run(self):
        dosya=open('rota.txt','w')
        dst_ip = socket.gethostbyname(self.dst)
        text = 'traceroute to {} ({}), {} hops max'.format(self.dst,dst_ip,self.hops)
        print(text)
        while True:
            startTimer = time.time()
            alici = self.alici_f() 
            gonderici = self.gonderici_f()
            gonderici.sendto(b'', (self.dst, self.port))

            addr = None
            try:
                data, addr = alici.recvfrom(1024) 
                entTimer = time.time()
            except socket.error as e:
                pass
                #raise IOError('Hata: {}'.format(e))
            finally:
                alici.close()
                gonderici.close()

            if addr:
                timeCost = round((entTimer - startTimer) * 1000, 2)
                print('{:<4} {} {} ms'.format(self.ttl, addr[0], timeCost))
                text='{:<4} {} {} ms'.format(self.ttl, addr[0], timeCost)
                dosya.write(text+"\n")
                if addr[0] == dst_ip:
                    break
            else:
                print('{:<4} *'.format(self.ttl))
                text='{:<4} *'.format(self.ttl)
                dosya.write(text+"\n")

            self.ttl += 1

            if self.ttl > self.hops:
                break
        dosya.close()

def main():
    if len(sys.argv) <= 1:
        print('Yanlış girdi. Lütfen doğru bir şekilde girin.')
        sys.exit(1)

    dest_addr = sys.argv[1]
    host = socket.gethostbyname(dest_addr)
    tracer=Tracer(dest_addr,30)
    tracer.run()

if __name__ == "__main__":
    main()
