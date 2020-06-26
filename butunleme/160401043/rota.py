


#HAZIRLAYAN
#ERENAY TOSUN - 160401043



import socket, os, random, struct, sys



SIZE = 1024


try:
    giris = sys.argv[1]
except:
    exit( '\nKomut girişi başarısız... sudo python3 rota.py "www.comu.edu.tr" olarak tekrar deneyiniz...' )
    
    

try:
    hedef = socket.gethostbyname( giris )
except socket.gaierror:
    exit( "\nHedef IP adresi bağlantısı başarısız..." )



def main():
    rotaDosya = open( "rota.txt", "w" )
    yonlendirici = 0
    TTL = 1
    
    while( yonlendirici != hedef ):
        gonder = 0
        devam = 1
        while( devam == 1 ):
            try:
                soket = socket.socket( socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP )
                zamanBitimi = struct.pack("ll", 2, 0)
                soket.setsockopt( socket.SOL_SOCKET, socket.SO_RCVTIMEO, zamanBitimi )
                soket.bind( ( '', 0 ) )

                udpSoket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP )
                udpSoket.setsockopt( socket.SOL_IP, socket.IP_TTL, TTL ) 
                udpSoket.sendto( b'data', ( hedef, random.choice( range( 33434, 33535 ) ) ) )
                _, yonlendirici = soket.recvfrom( SIZE )
                yonlendirici = yonlendirici[0]
                print( "Yönlendirici IP adresi: ", yonlendirici )
                rotaDosya.write( "{}\n".format( yonlendirici ) )
                break
                
            except socket.error:
                print( "\nTekrardan gönderme işlemi yapılıyor.." )
                pass
                
            finally:
                soket.close()
                udpSoket.close()

            gonder = gonder + 1
            
            if ( gonder == 3 ):
                devam = 0

        if ( TTL == 31 ):
            print( "\nTTL sınırına ulaşıldı !!!" )
            break
        TTL = TTL + 1

    rotaDosya.close()

if __name__ == "__main__":
    main()
    print( "\nYönlendirici IP adresleri 'rota.txt' dosyasına yazdırılmıştır.." )
    
    
    
    
    
    
    

