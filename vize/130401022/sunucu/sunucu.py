import socket
import os                       #HASAN SESLİ
import sys
import time
import scapy
        #HASAN SESLİ
#Önce sunucu.py daha sonra istemci.py dosyasını çalıştırın
sock_ip="127.0.0.1"
sock_port=42

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((sock_ip,sock_port))

veri , istemciAdresi = sock.recvfrom(4096)
print("Mesaj:" ,str(veri))
m="istemci sunucuya baglandi.."
message=bytes(m, encoding="utf8")
sock.sendto(message,istemciAdresi)

def sunucuGet(gelen):
    yol='/Users/TheSesli/Desktop/veriHaberlesmesi_sunucu/dosyalar/'+ str(gelen) #sunucu.py dosyasının olduğu dizin
    if os.path.isfile(yol):
        mesaj3="dosya mevcut"
        msj3=mesaj3.encode('utf8')
        sock.sendto(msj3, istemciAdresi)
        #eğer dosya mevcut ise
        dosya=os.stat(yol)
        dosyaB=dosya.st_size #dosyanın içerdiği paket sayısı (bayt olarak)
        boyut=int(dosyaB / 4096) #4096 size belirlediğimiz için bu şekilde int yapıyoruz 
        boyut= boyut +1  #gönderimdeki paketleri sayabilmek için
        devam=str(boyut) #encoding yapmak için
        devam2=devam.encode('utf8')
        sock.sendto(devam2,istemciAdresi)
        kontrolcu = int(boyut)
        dosyaİslemi = open(yol,"rb") #okuma izni ile gelen dosyayı açtık
        while kontrolcu != 0:
            dosyaİslemi2=dosyaİslemi.read(4096) #4096 bayt kullanıyoruz
            sock.sendto(dosyaİslemi2,istemciAdresi)
            kontrolcu = kontrolcu - 1
        dosyaİslemi.close()
    else:
        mesaj="Dosya adini yanlis girdiniz ya da dosya mevcut degil\n"
        msj=mesaj.encode('utf8')
        sock.sendto(msj, istemciAdresi)
def sunucuPut():
    if(islemD[0]=="put"):
        gelenMesaj, istemciAdresi = sock.recvfrom(4096)
        metin=gelenMesaj.decode('utf8')
        print(metin)
        if(metin=="dosya mevcut"):
            print("dosya mevcut")
            dosyaAc= open(islemD[1],"wb")
            paketSayisi , istemciAdresi = sock.recvfrom(4096)
            devam=paketSayisi.decode('utf8')
            devam2=int(devam)
            while devam2 != 0:
                sunucuVeri , istemciAdresi = sock.recvfrom(4096)
                dosyaVeri= dosyaAc.write(sunucuVeri)
                devam2= devam2 - 1
                dosyaAc.close()
            print("Yeni dosya yüklendi, listeyi kontrol edebilirsiniz\n")
        else:
            print(metin+"\n") 
def baglantiyiKes():
    metin, istemciAdresi=sock.recvfrom(4096)
    print("Mesaj : ",str(metin))
    msj="Server baglantiyi sonlandirdi.."
    mesaj=msj.encode('utf8')
    sock.sendto(mesaj,istemciAdresi)
    sock.close()
def hata():
    msj="Hata: sistem girdiniz '" + secilenİslem + "' komutunu algilamadi..Lütfen kuralli girdiginizden emin olun.."
    mesaj=msj.encode('utf8')
    sock.sendto(mesaj,istemciAdresi)
    print("\nHatali komut girildi..\n")

while True:

    sunucuDosyalari = os.listdir(path="C:/Users/TheSesli/Desktop/veriH_server/server_files")
    Liste = []
    print("Dosyalari listele..\n")

    for dosya in sunucuDosyalari:
        Liste.append(dosya) #Liste içine sunucu dosyalarını tek tek ekliyoruz
    listeString=str(Liste)
    listeCozum=listeString.encode('utf8')
    mesaj2=bytes("Sunucudaki dosyalar listeleniyor..", encoding='utf8')
    sock.sendto(mesaj2,istemciAdresi)
    sock.sendto(listeCozum,istemciAdresi)

    veri,istemciAdresi=sock.recvfrom(4096)
    secilenİslem= veri.decode('utf8')
    if(secilenİslem.startswith("get[")):
        islemD=secilenİslem.split("[")
        islemD[1]=islemD[1].strip("]")
        if(islemD[0]== "get"):
            sunucuGet(islemD[1])
    elif(secilenİslem.startswith("put[")):
        islemD=secilenİslem.split("[")
        islemD[1]=islemD[1].strip("]")
        if (islemD[0] =="put"):
            sunucuPut()
    
    elif (secilenİslem.startswith("cikis[")):
        islemD=secilenİslem.split("[")
        islemD[1]=islemD[1].strip("]")
        if(islemD[1]=="quit"):
            baglantiyiKes()
            break
    else:
        hata()
