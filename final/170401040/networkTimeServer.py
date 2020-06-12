import socket, os, time, sys
from datetime import datetime, timezone, timedelta

IP = str(socket.gethostbyname(socket.gethostname() + ".local"))
PORT = 142
SIZE = 2048


def select_time_zone():  # Kullanicidan zaman dilimi bilgisi alan fonksiyon

    UTC = int(input("Zaman dilimini seciniz: UTC "))  # +2 veya -3 gibi..
    return UTC

def calculate_RTT(client, UTC):  # Round Trip Time (Gidis Donus Suresi) hesaplayan fonksiyon

    if (UTC < 0):
        timezone = " UTC " + str(UTC)
    else:
        timezone = " UTC +" + str(UTC)

    firstTime = datetime.utcnow() + timedelta(hours=UTC)
    client.send(
        bytes(str(firstTime) + timezone, encoding='utf-8'))  # RTT'yi kontrol etmek icin istemciye veri gonderilir
    control = client.recv(SIZE)  # RTT'yi kontrol etmek icin istemciden veri alinir
    lastTime = datetime.utcnow() + timedelta(hours=UTC)

    rtt = lastTime - firstTime  # RTT icin veri gonderme alma islemleri arasindaki zamanlar birbirinden cikarilir
    return rtt

def main():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((IP, PORT))
    except:
        print("\n!!! HATA: Sunucu olusturma basarisiz oldu. Tekrar deneyiniz..")
        sys.exit()

    print("\n------- Sunucu hazir durumda -------\n")

    server.listen(1)
    client, clientAddress = server.accept()
    print(">> Istemci ile baglanti basariyla gerceklesti..\n\n------------------------------------\n")

    UTC = select_time_zone()  # Zaman dilimi bilgisini kullanicidan alir. (+2 veya -3 gibi)
    if (UTC < 0):
        print("\nSecilen zaman dilimi >> UTC " + str(UTC))
    else:
        print("\nSecilen zaman dilimi >> UTC +" + str(UTC))

    print("\n------------------------------------\n")

    rtt = calculate_RTT(client, UTC)  # Round Trip Time (Gidis Donus Suresi)
    delay = rtt / 2  # Tek yonlu gecikme
    print("Tek Yonlu Gecikme Suresi >> ", delay)

    TIME = datetime.utcnow() + timedelta(hours=UTC) + delay  # Gecikme ile hesaplanmis zaman
    TIME = str(TIME.strftime("%d %B %Y ")) + str(datetime.time(TIME))

    client.send(bytes(TIME, encoding='utf-8'))
    print("\nGecikmeli Sunucu Zamani >> ", TIME)

    if (UTC < 0):
        timezone = " UTC " + str(UTC)
    else:
        timezone = " UTC +" + str(UTC)

    client.send(bytes(timezone, encoding='utf-8'))

    print("\n------------------------------------\n\n>> Sunucu kapaniyor..")
    client.close()
    server.close()
    print("\n---------- Sunucu kapandi ----------\n")


if __name__ == "__main__":
    main()
    