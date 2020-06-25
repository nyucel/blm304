import sys
import socket
import struct

#Oğuz Demirhan - 160401050

hedef = socket.gethostbyname(sys.argv[1])

#dosya = open("test.txt",mode='a',encoding='utf-8')

#dosya.write(str(hedef))

dosya = open("rota.txt", mode='a', encoding='utf-8') # Dosya append modunda açıldı. Eğer dosya mevcut değil ise yaratıldı.


dosya.write(sys.argv[1])
dosya.write(",Hedef IP:")
dosya.write(str(hedef))
dosya.write("\n")



maksimum_deneme = 30

port = 33434

icmp = socket.getprotobyname('icmp') #icmp nesnesi yaratıldı
udp = socket.getprotobyname('udp') #udp nesnesi yaratıldı
ttl = 1         #1 den başlayarak maksimum deneme sayısına yani 30a kadar artacak.

while True:
    #raw soket oluşturuldu ve icmp ile ilişkilendirildi.
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    #send soket oluşturuldu ve udp ilişkilendirildi.
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
    #
    send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)


    # Yönlendiriciye deneme yapılırken kullanmak için bir zaman aşımı değişkeni tanımladım.
    zamanAsimi = struct.pack("ll", 3, 0)


    # Tanımladığım zaman aşımı değerini alıcı soket üzerinde kullandım.

    recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, zamanAsimi)

    recv_socket.bind(("", port))
    #belirtilen adrese dummy bir veri gönderilir.
    send_socket.sendto(b"dummy", (sys.argv[1], port))

    adres = None
    isim = None
    bittimi = False
    deneme = 3


#Bilgisayar veri alana ya da deneme 0 olana kadar çalışmaya devam eder.
    while not bittimi and deneme > 0:
        try:
            _, adres = recv_socket.recvfrom(512)
            bittimi = True
            adres = adres[0]
            try:
                isim = socket.gethostbyaddr(adres)[0]
            except socket.error:
                isim = adres
        except socket.error:
            #Yönlendiriciden yanıt alınamazsa deneme 1 azaltılır ve döngüden çıkılır.
            deneme = deneme - 1

#Açılan soketler kapatılır.

    send_socket.close()
    recv_socket.close()

    if not bittimi:
        pass

    if adres is not None:
        #Bulunan adres .txt uzantılı dosyaya yazılır.
        print("TTL->",ttl,str(adres))
        #print(str(adres))
        dosya.write(str(adres))
        dosya.write("\n")

    ttl += 1
    if adres == hedef or ttl > maksimum_deneme:
        break

dosya.write("\n")
dosya.close()




