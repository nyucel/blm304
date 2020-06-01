import socket
import os
import sys
#160401019
#Sena Günay

def dosyalari_listele():

    dosyalar = os.listdir(os.getcwd())
    Liste = []

    for dosya in dosyalar:
        Liste.append(dosya)

    ListeStr = str(Liste)
    ListeEncode = ListeStr.encode('utf-8')
    s.sendto(ListeEncode, addr)
    print("Liste server tarafindan yollaniyor.")

def GET(gonderilecek_dosya):
    if(gonderilecek_dosya in os.listdir()):
        dosya = open(gonderilecek_dosya,"rb")
        dosya2 = dosya.read()
        try:
            s.sendto(dosya2,address)
        except:
            print("Dosya istemciye gonderilemedi.")
            sys.exit()
    else:
        print("Bu isimde bir dosya bulunamadi")
        sys.exit()

def PUT(yuklenecek_dosya):
    veri,address=s.recvfrom(4096)
    dosya=open(yuklenecek_dosya,'wb')
    dosya.write(veri)
    dosya.close()
    print("Yükleme tamamlandi")

host = "127.0.0.1"
port = 4242

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("socket oluşturuldu")

    s.bind((host, port))
    print("socket {} nolu porta bağlandı".format(port))

except socket.error as msg:
    print("Hata:",msg)


# Client ile bağlantı kurulursa
c, addr = s.recvfrom(4096)
print('Gelen bağlantı:', addr)
print(c)
mesaj = ("Baglanti icin tesekkurler. Islem yapabileceginiz dosyalar asagidaki gibidir: ").encode('utf-8')
s.sendto(mesaj,addr)
dosyalari_listele()

cli,adress = s.recvfrom(4096)
komut= cli.decode('utf-8')

if(komut=="GET"):
    dosya_adi, address = s.recvfrom(4096)
    dosya_adi = dosya_adi.decode('utf-8')
    GET(dosya_adi)
elif(komut=="PUT"):
    p_dosya_adi, address = s.recvfrom(4096)
    p_dosya_adi = p_dosya_adi.decode('utf-8')
    PUT(p_dosya_adi)

