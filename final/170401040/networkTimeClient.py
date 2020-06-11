import socket, os, time, sys
from os import system, name
from datetime import datetime, timedelta

IP = '10.0.2.15'
PORT = 142
SIZE = 2048


def clear():  # Terminal ekranini temizleme fonksiyonu

    if (name == 'nt'):
        _ = system('cls')
    else:
        _ = system('clear')

def update_time_on_Linux(currentTime):  # Linux uzerinde zaman guncellemesi yapan fonksiyon

    date = currentTime.split(" ")
    date = date[0] + " " + date[1] + " " + " " + date[2] + " " + date[3] + " "

    try:
        os.system('date --set "%s" +\"%%d %%B %%Y %%H:%%M:%%S.%%6N\"' % date)
        os.system("sudo hwclock -w")
        print("\n>> Sistem zamani basariyla guncellendi <<\n")
    except:
        print("\n>> Sistem zamani guncellenemedi..\n")

def main():
    try:
        client = socket.socket()
    except:
        print("!!! HATA: Istemci olusturma basarisiz oldu. Tekrar deneyiniz..")
        sys.exit()

    print("\n>> Istemci basariyla olusturuldu..\n")

    try:
        client.connect((IP, PORT))
    except:
        clear()
        print("\n!!! HATA: Sunucu hazir değil. İlk olarak sunucuyu hazir ediniz..\n")
        sys.exit()

    print(">> Sunucu ile istemci arasinda baglanti kuruldu..")

    print("\n====================================================\n")

    print(">> Sunucuda zaman dilimi secimi yapiliyor..")

    remoteTime = client.recv(SIZE)  # Gecikmes suresi kontrolu icin sunucudan veri alinir
    client.send(bytes("tamam", encoding='utf-8'))  # Gecikme suresi kontrolu icin sunucuya veri gonderilir

    print("\nIstemci Zamani: " + str(datetime.now().strftime("%d %B %Y %H:%M:%S.%f ")) + "UTC +3")

    currentTime = client.recv(SIZE)
    timezone = client.recv(SIZE)

    print("\nSunucu Zamani: " + currentTime.decode("utf-8") + timezone.decode("utf-8"))

    print("\n====================================================\n")

    print(">> Istemci kapandi..")

    print("\n====================================================\n")

    print(">> Sistem saati guncelleniyor..\n")

    update_time_on_Linux(currentTime.decode("utf-8"))  # Linux uzerinde istemci zamani sunucu zamani ile guncellenir

if __name__ == "__main__":
    main()


