import socket
import struct
import sys
BUFFER_BOYUTU = 1024

#BAHAR ÇİFTÇİ

class traceroute(object):

    def __init__(self,makine_adi,yonlendirici=30):
        self.makine_adi = makine_adi
        self.yonlendirici = yonlendirici
        self.ttl = 1
        self.port = 33503
    
    def alici_İCMP_paket(self):
        icmp = socket.socket(family=socket.AF_INET,type=socket.SOCK_RAW,proto=socket.IPPROTO_ICMP)
        zamanAsimi = timeout = struct.pack("ll", 280, 0)
        icmp.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, zamanAsimi)
        icmp.bind(('', self.port))

        return icmp

    def gonderici_UDP_paket(self):
        udp = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM,proto=socket.IPPROTO_UDP)
        udp.setsockopt(socket.SOL_IP, socket.IP_TTL, self.ttl)

        return udp
    
    def ROTA(self):

        dosya=open('rota.txt','w')
        destination_ip = socket.gethostbyname(makineAdi)
        print("Makine adi : %s  , ip'si : %s   traceroute işlemi gerçeklestiriliyor.." %(self.makine_adi, destination_ip))

        while True:

            icmp = self.alici_İCMP_paket()
            udp = self.gonderici_UDP_paket()

            udp.sendto(b'', (self.makine_adi, self.port))

            adres = None

            try:
                mesaj , adres = icmp.recvfrom(BUFFER_BOYUTU)
            
            except socket.error as e:
                print(e)

            finally:
                icmp.close()
                udp.close()

            if (adres):
                metin = "Ttl degeri = %s ,  yonlendirici İp'si : %s" %(self.ttl, adres[0])
                print(metin + "\n")
                dosya.write(metin + "\n")
                if (adres[0] == destination_ip):
                    break
            
            else:
                metin = "Ttl degeri = %s ,  yonlendirici İp'si : ** " %(self.ttl)
                print(metin + "\n")
                dosya.write(metin + "\n")

            self.ttl = self.ttl +1

            if self.ttl > self.yonlendirici:
                break
        
        dosya.close()


if __name__ == "__main__":

    if len(sys.argv) <= 1 :
        print("\nMakina adini yanlis yada eksik girdiniz.. tekrar acip tekrar deneyin\n")
        sys.exit(1)
    
    makineAdi = sys.argv[1]
    
    try:
            
        destination_ip = socket.gethostbyname(makineAdi)
            

    except:
        print("\nMakina adini yanlis girdiniz yada hedef ip cözümlenemedi..\n")
        print("\nMakina adini dogru girerek tekrar deneyin..\n")
        sys.exit(1)

    else:
        rotaTakip = traceroute(makineAdi,30)
        rotaTakip.ROTA()
