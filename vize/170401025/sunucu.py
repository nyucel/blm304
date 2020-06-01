import socket
import sys
import os

def listele():
    liste = os.listdir(os.getcwd())
    dosya=[]
    for i in liste:
        if(i!= "sunucu.py"):
            dosya.append(i)
    dosya1=(str(dosya).encode('utf-8'))
    try:
        s.sendto(dosya1,address)
    except:
        print("Baglanti hatasi")
        sys.exit()

def GET(dosyaAdi):
    if(dosyaAdi in os.listdir()):
        dosya=open(dosyaAdi,"rb")
        veri=dosya.read()
        try:
            s.sendto(veri,address)
        except:
            print("Baglanti Hatasi")
            sys.exit()
    else:
        mesaj="Dosya bulunamadi"
        mesaj=mesaj.encode('utf-8')
        s.sendto(mesaj,address)
def PUT(dosya_adi):
    data,address=s.recvfrom(4096)
    f=open(dosya_adi,'wb')
    f.write(data)
    f.close()
    try:
        mesaj="Yükleme tamamlandi"
        mesaj=mesaj.encode('utf-8')
        s.sendto(mesaj,address)
    except:
        print("Baglanti hatasi")
        sys.exit()


host="127.0.0.1"
port=42

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Sunucu soketi baslatildi.")
    s.bind((host,port))
    print("Baglama basarili")
except:
    print("Soket olusturulamadi.")
    sys.exit()

while True:
    try:
        c, address = s.recvfrom(4096)
        print('Gelen baglanti: ', address)
    except:
        print("Bağlanti Hatasi")
        sys.exit()
    data=c.decode('utf-8')
    if(data=="List"):
        listele()

    elif(data=="GET"):
        dosyaAdi,address=s.recvfrom(4096)
        dosyaAdi=dosyaAdi.decode('utf-8')
        GET(dosyaAdi)

    elif(data=="PUT"):
        p_dosyaAdi,address=s.recvfrom(4096)
        p_dosyaAdi=p_dosyaAdi.decode('utf-8')
        if (p_dosyaAdi in os.listdir()):
            mesaj = "Dosya zaten sunucu dizininde mevcut."
            mesaj = mesaj.encode('utf-8')
            s.sendto(mesaj,address)
        else:
            mesaj="İslem onay"
            mesaj = mesaj.encode('utf-8')
            s.sendto(mesaj,address)
            PUT(p_dosyaAdi)
    elif(data=="-1"):
        print("İslem Sonlaniyor...")
        sys.exit()
    else:
        print("Yanlis komut girisi")




