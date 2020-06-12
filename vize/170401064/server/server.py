# 170401064 Meyra Aslıhan

# sudo python3 client.py --server 192.168.62.164 --iface ens33
# sudo python3 server.py --iface ens33

from scapy.all import *
from subprocess import Popen, PIPE
import time
import argparse
import os

if os.geteuid() != 0:
    exit("sudo ile kullanın")

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--iface', help='Interface', nargs=1, type=str, required=True)
args = arg_parser.parse_args()
conf.verb = 0

print("Server çalışıyor...")

def send_response(res):
    pck=IP(dst=master)/UDP(dport=master_port, sport=42)/Raw(load="verihaberlesmesi"+res) # server 42 portu üzerinden udp paketini gönderiyor.
    send(pck)
    print("Yanıt Gönderildi")

def sniff_packet():
    pck = sniff(session=IPSession, count=1, filter="udp", iface=args.iface[0])
    try:
        master = pck[0][IP].src
    except:
        master = None
    master_port = pck[0].sport

    try:
        data = pck[0].load
    except AttributeError:
        data = None

    return data, master_port, master

while True:
    try:
        data, master_port, master = sniff_packet()
    except IndexError:
        print("Server Durduruldu!")
        break
    
    time.sleep(0.4)
    if(data is not None and master is not None):
        kontrol = data[:16]
        islem = data[16:]
        if kontrol == b'verihaberlesmesi': # client tarafından gelen verinin baş kısmında 'verihaberlesmesi' stringi check ediliyor.
            parcala = islem.split(b' ',1)
            komut = str(parcala[0],"utf-8")

            if komut == 'cikis':
                send_response("Server Kapatildi")
                break
            elif komut == "put":
                data = parcala[1].split(b' ',1)
                f = open(data[0], "wb")
                f.write(data[1])
                f.close()
                send_response("Dosya Kaydedildi")
            elif komut == "get":
                try:
                    with open(parcala[1], mode='rb') as file:
                        fileContent = file.read()
                        pck=IP(dst=master)/UDP(dport=master_port,sport=42)/Raw(load=b'verihaberlesmesi'+fileContent) # server 42 portu üzerinden get komutundan talep edilen dosyayı udp ile gönderiyor
                        send(pck)
                        print("Yanit Gonderildi")
                except FileNotFoundError:
                    print("Dosya Bulunamadi.")
                    send_response("hata")
                except struct.error:
                    print("Dosya boyutu en fazla 65536 byte olabilir.")
                    send_response("buyuk")
            elif komut == "list": # kullanıcıdan gelen listeleme işlemi için ls komutu çalıştırılıyor
                proc = Popen("ls", shell=True, stdout=PIPE, stderr=PIPE)
                res = str(proc.stdout.read()+proc.stderr.read(),"utf-8")
                send_response(res)
            else:
                print("Hatali Istek")
                send_response("Hatali Istek")
