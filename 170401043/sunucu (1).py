import socket
import os

#Merve Öztürk
#170401043

host = input("Ip giriniz:")
port = 42
global dosyalistesi
def socket_islenleri():
    global sock
    global c
    global adres
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        print("{}. porta bağlandı".format(port))
        sock.listen(5)
        print("socket dinleniyor")
        while True:
            c, adres = sock.accept()
            print('Gelen bağlantı:', adres)
            mesaj = 'Bağlantı için teşekkürler'
            c.send(mesaj.encode('utf-8'))

    except socket.error as hata:
        print("socket olusturulamadı... \nHata:",hata)



def put_fonk(filename):
    say = 0
    for i in os.listdir(os.getcwd()):
        if i.startswith("dosya"):
            say += 1
    dosya_no = say

    print("Sunucu açıldı...\n bekleniyor...")
    global c
    global adres
    while True:
        datas = c.recv(1024)
        file = open(filename.format(dosya_no), "wb")
        while datas:
            file.write(datas)
            datas = c.recv(1024)
        file.close()
        dosyalistesi.add(filename)
        print("dosya alındı...")
        dosya_no += 1
        continue

def get_fonk(filenames):

    filename = open(filenames, "rb")
    data = filename.read()

    while data:
        sock.send(data)
        data = filename.read()

    filename.close()
    print("Dosya gönderildi.")
    print("\n")

def listele():
    dosyalar=open("dosyalar.txt","w")
    for i in dosyalistesi():
        dosyalar.write(i)

    dosyalar.close()


def islemler():
    send_dir = os.getcwd()
    c.send(str.encode(str(send_dir)))
    while True:
        data = c.recv(1024)
        data = data.decode("utf-8")
        komut_ayir = data.split(" ")
        cm = komut_ayir[0]

        try:
            filename = komut_ayir[1]
        except:
            filename = ""

        if (cm == "get"):
            get_fonk()

        elif (cm == "put"):
            put_fonk()
        elif (cm == "ls"):
            listele()
        else:
            print()
            sock.close()

socket_islenleri()
islemler()