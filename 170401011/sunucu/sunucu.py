#170401011 Berfin Okuducu
import socket
import sys
import os

def list():
    listing = os.listdir(os.getcwd())
    File=[]
    for i in listing:
        if(i!= "sunucu.py"):
            File.append(i)
    file=(str(File)).encode('utf-8')
    try:
        s.sendto(file,address)
    except:
        print("Baglanti hatasi")
        sys.exit()

def GET(dosya_adi):
    if(dosya_adi in os.listdir()):
        dosya=open(dosya_adi,"rb")
        veri=dosya.read()
        try:
            s.sendto(veri,address)
        except:
            print("Baglanti Hatasi")
            sys.exit()
    else:
        mesaj="Dosya sunucu dizininde bulunamadi"
        mesaj=mesaj.encode('utf-8')
        try:
            s.sendto(mesaj,address)
        except:
            print("Baglanti Hatasi")
            sys.exit()

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

baglanti,address=s.recvfrom(4096)
baglanti=baglanti.decode('utf-8')
print(str(baglanti))
mesaj="Baglanti icin tesekkurler"
mesaj=mesaj.encode('utf-8')
try:
    s.sendto(mesaj,address)
except:
    print("Baglanti Hatasi")
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
        list()

    elif(data=="GET"):
        try:
            dosya_adi,address=s.recvfrom(4096)
            dosya_adi=dosya_adi.decode('utf-8')
            GET(dosya_adi)
        except:
            print("Bağlanti Hatasi")
            sys.exit()

    elif(data=="PUT"):
        try:
            p_dosya_adi,address=s.recvfrom(4096)
        except:
            print("Bağlanti Hatasi")
            sys.exit()
        p_dosya_adi=p_dosya_adi.decode('utf-8')
        if (p_dosya_adi in os.listdir()):
            mesaj = "Dosya zaten sunucu dizininde mevcut."
            mesaj = mesaj.encode('utf-8')
            try:
                s.sendto(mesaj,address)
            except:
                print("Baglanti Hatasi")
                sys.exit()
        elif(p_dosya_adi=="Dosya Yok"):
            mesaj="Gönderilecek dosya istemci dizininde bulunamadi"
            mesaj = mesaj.encode('utf-8')
            try:
                s.sendto(mesaj, address)
            except:
                print("Baglanti Hatasi")
                sys.exit()
        else:
            mesaj="İslem onay"
            mesaj = mesaj.encode('utf-8')
            try:
                s.sendto(mesaj,address)
            except:
                print("Baglanti Hatasi")
                sys.exit()
            PUT(p_dosya_adi)
    elif(data=="-1"):
        print("İslem Sonlaniyor...")
        sys.exit()
    else:
        print("Yanlis komut girisi")











