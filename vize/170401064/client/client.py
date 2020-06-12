# 170401064 Meyra Aslıhan

# sudo python3 client.py --server 192.168.62.164 --iface ens33
# sudo python3 server.py --iface ens33

from sys import argv
from scapy.all import *
import random
import argparse
import os

if os.geteuid() != 0:
    exit("sudo ile kullanın")

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--server', help='Server Ip', nargs=1, type=str, required=True)
arg_parser.add_argument('--iface', help='Interface', nargs=1, type=str, required=True)
args = arg_parser.parse_args()
conf.verb = 0

print("""
Kullanimi:
list            Dizinde yer alan dosyalari listeler
put dosyaAdi    Dosya Yuklemek icin
get dosyaAdi    Dosya Cekmek icin
cikis           Cikis Islemi icin
-------------------------------------------------------
""")

def send_packet(data):
    pck=IP(dst=args.server[0])/UDP(dport=42,sport=source_port)/Raw(load=data) # paketimiz server'ın 42. portuna udp ile gönderiliyor
    send(pck)

def sniff_packet():
    pck = sniff(session=IPSession, count=1, filter="udp", iface=args.iface[0], timeout=4)

    if not pck:
        return None

    try:
        res = pck[0].load

        if res[:16] == b'verihaberlesmesi':
            return res[16:]
    except AttributeError:
        return None

# client'ın dinleyeceği port oluşturuluyor
source_port = random.randint(2000, 65536)

while True:
    try:
        inputData = input('$ ')
    except KeyboardInterrupt: # uygulama durdurulursa
        print("Client Durduruldu!")
        break

    data = None
    command = inputData.split(' ', 1)[0] # kullanıcının input'u boşluk karakteri ile parse ediliyor ve ilk kısmı alınıyor. bu kısım, kullanılacak komuttur.

    if command == "put": # yazılan komut put ise
        path = inputData.split(' ', 1)[1] # parse edilen input'un ikinci kısmı, put ile gönderilecek dosyamızın yoludur
        dosyaAdi = path
        try:
            with open(dosyaAdi, mode='rb') as file:
                fileContent = file.read()
                data = b'verihaberlesmesiput ' + dosyaAdi.encode() + b' ' + fileContent # gönderilecek verinin başına 'verihaberlesmesi' stringi eklenir ve sonra yazdığımız komut, dosya adı ve dosya içeriği eklenerek gönderilir.
                send_packet(data)
        except FileNotFoundError: # eğer dosya yok ise
            print("Bu isimde dosya bulunamadi.")
            continue
        except struct.error: # scapy de udp ile gönderilen dosya boyutu max 65536 byte olabilir, büyük gelirse uyarı çıkartıyor.
            print("Gonderilen dosya boyutu en fazla 65536 byte olabilir.")
            continue
    else:
        data = "verihaberlesmesi" + inputData # girilen komut put değil ise kullanıcı girdisinin başına 'verihaberlesmesi' stringi eklenir, sebebi: iletişim sırasında başka uygulamadan gelen istekler ile karışmaması ve düzgün çalışması içindir.
        send_packet(data)

    i = 1
    response = sniff_packet()
    while response == None and i <= 5: # bağlantı kopması sonucu kaldığı yerden devam etmesi için 5 kez tekrar göndermeyi deniyor. kesintisiz iletişim için.
        print("Tekrar Deneniyor " + str(i))
        if(data != None):
            send_packet(data)
        i+=1
        response = sniff_packet()

    if response == None:
        print("Zaman Asimi")
        continue

    if command == "get": # kullanıcı get komutunu kullanmış ise 
        path = inputData.split(' ', 1)[1] # kullanıcı girdisinin ikinci kısmı yani dosya yolu parse ediliyor

        if response == b'hata':
            print("Bu isimde dosya bulunamadi.")
            continue
        elif response == b'buyuk':
            print("Alinan dosya boyutu en fazla 65536 byte olabilir.")
            continue

        filename = path
        f = open(filename, "wb")
        f.write(response)
        f.close()
        print("Dosya Kaydedildi")
    elif command == "cikis":
        print(str(response,"utf-8"))
        exit()
    else:
        print(str(response,"utf-8"))
