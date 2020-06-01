'''
Atakan Ayaşlı 170401066
'''
import socket
import time
import os
import sys

def Dosya_listele():

    msg = "LİSTE Komutu doğru"
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
    F = os.listdir(
        path="C:\Users\Atakan\Desktop\170401066\server")
    """ lütfen server.py dosyasının olduğu path'i yazınız eğer unicode hatası alıyorsanız pathi yazarken başlangıca r koyunuz örnek= r"C:/Users/...."
    """
    Lists = []
    for file in F:
        Lists.append(file)
    ListsStr = str(Lists)
    ListsEn = ListsStr.encode('utf-8')
    s.sendto(ListsEn, clientAddr)

def PUT():

    msg = "Kabul edilen PUT komutu"
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
    if t2[0] == "PUT":
        BigSAgain = open(t2[1], "wb")
        d = 0
        print("Transfer başlıyor")
        try:
            Count, countaddress = s.recvfrom(4096)
        except ConnectionResetError:
            print(
                "Port numaraları uyuşmuyor.")
            sys.exit()
        except:
            print("Bilinmeyen Hata")
            sys.exit()
        tillI = Count.decode('utf8')
        tillI = int(tillI)

        while tillI != 0:
            ServerData, serverAddr = s.recvfrom(4096)
            dataS = BigSAgain.write(ServerData)
            d += 1
            tillI = tillI - 1
            print("Alınan Paket numarası:" + str(d))
        BigSAgain.close()
        print("Son")

def Exit():
    print("Çıkış")
    s.close()
    sys.exit()

def ipkontrol():
    if len(sys.argv) != 2:
        print(
            "lütfen ip giriniz(server.py 127.0.0.1)!/\n Eğer server.py dosyasınının 16. satırınının dosya pathini manuel ayarlamadıysanız hata verebilir path'i server.py'ın bulunduğu klasörün pathini manuel yazınız ")
        sys.exit()

def GET(g):
    msg = "Kabul edilen komut "
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)

    if os.path.isfile(g):
        msg = "Dosya bulundu. "
        msgEn = msg.encode('utf-8')
        s.sendto(msgEn, clientAddr)
        c = 0
        sizeS = os.stat(g)
        sizeSS = sizeS.st_size
        print("File size in bytes:" + str(sizeSS))
        NumS = int(sizeSS / 4096)
        NumS = NumS + 1
        tillSS = str(NumS)
        tillSSS = tillSS.encode('utf8')
        s.sendto(tillSSS, clientAddr)
        check = int(NumS)
        GetRunS = open(g, "rb")
        while check != 0:
            RunS = GetRunS.read(4096)
            s.sendto(RunS, clientAddr)
            c += 1
            check -= 1
            print("Paket numarası:" + str(c))
        GetRunS.close()
        print("Sn")

    else:
        msg = "Hata:dosya bulunamadı"
        msgEn = msg.encode('utf-8')
        s.sendto(msgEn, clientAddr)

def Else():
    msg = "istediğniz " + \
        t2[0] + " server tarafından anlaşılmadı"
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
host = ""
ipkontrol()
port=42

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    print("Başarılı birleşme. Şimdi client bekleniyor.")
except socket.error:
    print("Hata")
    sys.exit()


while True:
    try:
        data, clientAddr = s.recvfrom(4096)
    except ConnectionResetError:
        print(
            "Port numaraları uyuşmuyor")
        sys.exit()
    text = data.decode('utf8')
    t2 = text.split()
    if t2[0] == "GET":
        GET(t2[1])
    elif t2[0] == "PUT":
        PUT()
    elif t2[0] == "LİSTE":
        Dosya_listele()
    elif t2[0] == "exit":
        Exit()
    else:
        Else()

print("Program sonlandırılıyor ")
quit()
