import socket
import os   #NOT   -------------  Sunucu ip si 127.0.0.1 girilmelidir
import sys
import time
                   #HASAN SESLİ

client_sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#paket iletimi için [buffer boyutu] = 4096 olarak girilmiştir..
while True:
    ip=input("Sunucu ip adresini kurallı olarak girin: ")
    if(ip=="127.0.0.1"):
        break
    else:
        print("Yanlis sunucu ip girdiniz!!\n")
        continue

message2="istemci sunucuya baglanmak istiyor.."
client_sock.sendto(message2.encode('utf8'),(ip,42))
veri,serverAdres=client_sock.recvfrom(4096)
metin=veri.decode('utf8')
print(metin+"\n")

while True:


    gelenMesaj, serverAdres=client_sock.recvfrom(51200)
    metin=gelenMesaj.decode('utf8')
    print(metin)
    gelenListe,serverAdres=client_sock.recvfrom(4096)
    Liste=gelenListe.decode('utf8')
    print(Liste)

    secim = input(
        "\nYapmak istediginiz islemi kurallı şekilde yazın!! : (1) get[dosya adi]  (2) put[dosya adi] (3) cikis[quit] : \n"
    )
    islemSonucu = secim.encode('utf8')
    client_sock.sendto(islemSonucu,("127.0.0.1",12347))
    if(secim.startswith("get[")):
        islemClient= secim.split("[")
        islemClient[1]=islemClient[1].strip("]")
        if(islemClient[0]=="get"):
            veri , serverAdres = client_sock.recvfrom(53800) # olabildiğince büyük boyutta bayt girdik
            gelenMetin = veri.decode('utf8')
            if (gelenMetin == "dosya mevcut"): 
                if(islemClient[0]=="get"):
                    alinanPaket= open("AlinanDosya-" +islemClient[1],"wb") #yazma izni
                    paketSayisi, paketAdresi = client_sock.recvfrom(4096)
                    devam=paketSayisi.decode('utf8')
                    devam2=int(devam)
                    while devam2 != 0:  #alınan paketi işliyoruz
                        veri2, serverAdres = client_sock.recvfrom(4096)
                        veriSonuc=alinanPaket.write(veri2)
                        devam2= devam2 -1
                    alinanPaket.close()
                    print("dosya alindi klasörü kontrol edin..")
            else:
                print(gelenMetin+"\n")
    elif(secim.startswith("put[")):
        islemClient= secim.split("[")
        islemClient[1]=islemClient[1].strip("]")
        if(islemClient[0]=="put"):
            yol='/Users/TheSesli/Desktop/veriHaberlesmesi_istemci/dosyalar/'+ str(islemClient[1])
            if os.path.isfile(yol):
                m="dosya mevcut"
                mesaj=m.encode('utf8')
                client_sock.sendto(mesaj,serverAdres)
                boyut=os.stat(islemClient[1])
                boyut2=boyut.st_size #byte olarak
                toplamPaket=int(boyut2 / 4096)
                toplamPaket = toplamPaket +1
                devam=str(toplamPaket)
                devam2=devam.encode('utf8')
                client_sock.sendto(devam2,serverAdres)
                devamKosul=int(toplamPaket)
                dosyaAc = open(islemClient[1], "rb")
                while devamKosul != 0:
                    ac = dosyaAc.read(4096)
                    client_sock.sendto(ac,serverAdres)
                    devamKosul= devamKosul -1
                dosyaAc.close()
                print("Dosya servere yüklendi dizini kontrol ediniz..\n")
            else:
                m2="dosya mevcut degil"
                mesaj2=m2.encode('utf8')
                client_sock.sendto(mesaj2,serverAdres)
                print("Dosya adini yanlis girdiniz ya da dosya mevcut degil\n")
    elif(secim.startswith("cikis[")):
        islemClient= secim.split("[")
        islemClient[1]=islemClient[1].strip("]")
        if(islemClient[1]=="quit"):
            msj="istemci baglantiyi sonlandirmak istiyor.."
            mesaj=msj.encode('utf8')
            client_sock.sendto(mesaj,serverAdres)
            metin, serverAdres = client_sock.recvfrom(4096)
            print(str(metin))
            client_sock.close()
            break
        else:
            print("cikis komutunu tam olarak dogru girmediniz!.. tekrar deneyin..\n")
    else:
        gelenMetin2,serverAdres = client_sock.recvfrom(4096)
        metin = gelenMetin2.decode('utf8')
        print("\n"+metin+"\n")
