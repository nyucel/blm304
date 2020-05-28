# Veri Habereşmesi Ödevi

BLM304 Rabia Kaynak - 160401091

## Hazırlıklar

- FTP server kurmadan önce iki makineyi haberleştirmek için sanal makine ayarlarından iyi makineyi aynı NAT ağında buluşturdum.

**Server**: 10.0.2.4

**Client**: 10.0.2.15

- Sonra iletişim kurup kuramadıklarını test etmek için client makineden server makineye ping attım. **tcpdump** ile server makineyi dinlediğimde icmp paketlerinin client makineden geldiğini gördüm.


![iptables kural tablosu](https://i.hizliresim.com/ih6Zou.jpg)

---

- Daha sonra sonra server ve client makinede arasındaki tcp bağlantısını engellemek için **iptables** ile iki makinede de şu kuralı yazdım.


```bash
iptables -A INPUT -s IP-ADDRESS -p tcp -j DROP
```

![iptables kural tablosu](https://i.hizliresim.com/pNmpvt.jpg)

---
- Sonrasında TCP bağlantısının kesilip kesilmediğini test etmek için client makineden 2399 portundan netcat ile bağlantı kurmaya çalıştım.

Client makineden aşağıdaki komutu yazıp:

```bash
nc localhost 2399
```

Server makineden:

```bash
nc -l 2399
```

komutu ile dinledim falat yazdığım mesajlar server'a ulaşmıyordu. aynı zamanda tcpdump ile de bunu teyit ettim.

---



## FTP Server Oluşturulması

Burada beni tuzağa düşüren şey portu **42** ayarlayınca yönetici izinine ihtiyaç duyulmasıydı. 1023 üzeri portlar izin istemezken altındaki portlar yönetici iznine ihiyaç duyuyor. **sudo** ile çalıştırılması gerekli.

```python
import socket
import os
import time

# Server IP ve PORT bilgisi:

IP = "10.0.2.4"
PORT = 42
bufferSize = 4096

# Server üzerinde directory oluşturulması

mainDirectory = os.listdir()
serverDirectory = "Server Directory"

if serverDirectory not in mainDirectory:
    os.mkdir(serverDirectory)
    print("Server Directory created.")
else:
    print("Directory already created. Passing...")
os.chdir(serverDirectory)


while True:

    # Bağlantının UDP üzerinden yapılabilmesi için:

    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPServerSocket.bind((IP, PORT))

    i = 0

    while i < 1:

        print("Server is listening...")
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

        message = bytesAddressPair[0].decode()

        address = bytesAddressPair[1]

        # Gelen komutu command: komut ve file_title: dosya adı şeklinde ayrımak için:

        command = message[:3]
        file_title = message[4:]

        # Client tarafından gelecek ilk istek directory'deki tüm dosyaları listeler

        if command == "LIST":

            msgFromServer = str(os.listdir())
            bytesToSend = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address)

        # Client tarafından GET komutu yapılması durumunda:

        elif command == "GET":

            allFiles = os.listdir()

            # Eğer dosya tüm dosyalar içinde varsa:

            if file_title in allFiles:

                file_name = file_title.encode()

                f = open(file_title, "rb")
                data = f.read(bufferSize)

                # Dosya ismi ve dosyanın yollanması

                UDPServerSocket.sendto(file_name, address)
                UDPServerSocket.sendto(data, address)

                while data:
                    if UDPServerSocket.sendto(data, address):
                        print("Wait...")
                        data = f.read(bufferSize)
                        time.sleep(0.01)

                # Komut iletilme durmunun kontrolü

                try:
                    UDPServerSocket.settimeout(3)
                    issended = UDPServerSocket.recvfrom(bufferSize)[0].decode()

                    if issended == "True":
                        
                        print("Succesfully sended.")

                except socket.timeout:

                    print("Failed to send file.")

                # Socket kapatıldı

                UDPServerSocket.close()
                f.close()

            # Eğer dosya yoksa

            else:
                UDPServerSocket.sendto(b"error", address)
                UDPServerSocket.close()

        # Client tarafından PUT komutu yapılması durumunda

        elif command == "PUT":

            data = UDPServerSocket.recvfrom(bufferSize)[0]
            f = open(data.strip(), "wb")

            data = UDPServerSocket.recvfrom(bufferSize)[0]
            try:
                while data:
                    data = UDPServerSocket.recvfrom(bufferSize)[0]
                    f.write(data)

                    # Timeout bitene kadar bağlantı sağlanmasının beklenmesi

                    UDPServerSocket.settimeout(3)

            except socket.timeout:
                f.close()

            UDPServerSocket.sendto(b"True", address)
            UDPServerSocket.close()

        i += 1
```


## FTP Client Oluşturulması

```python
import socket
import os
import sys
import time

ip = "localhost"
serverAddressPort = (ip, 42)
bufferSize = 4096

msgFromClient = "LIST"
bytesToSend = str.encode(msgFromClient)


# Bağlantının UDP üzerinden yapılabilmesi için:


UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:

    #  Dosyaların listelenmesi için ilk olarak LIST komutunu gönderiyoruz:

    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

except:

    #  Exception:

    print("Can't connect to server.")
    sys.exit()

msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Files {}".format(msgFromServer[0].decode())
print(msg)

#  Kullanıcıdan girdi alma:

command = input(
    "You can use the command line to use FTP server: 'COMMAND (PUT / GET) FILE_NAME'"
)

command = command.encode()
UDPClientSocket.sendto(command, serverAddressPort)

# GET komutu yapılması durumunda:

if command.find("GET") == 0:

    data = UDPClientSocket.recvfrom(bufferSize)[0]

    #  Eğer dosya bulunamazsa

    if data.decode() == "error":
        print("Not found.")

    #  Eğer dosya bulunması durumunda

    else:
        f = open(data.strip(), "wb")

        data = UDPClientSocket.recvfrom(bufferSize)[0]

        try:
            while data:
                data = UDPClientSocket.recvfrom(bufferSize)[0]
                f.write(data)

                # Timeout bitene kadar bağlantı sağlanmasının beklenmesi

                UDPClientSocket.settimeout(3)

        except socket.timeout:

            f.close()

        UDPClientSocket.sendto(b"True", serverAddressPort)
        UDPClientSocket.close()

# PUT komutu yapılması durumunda:

elif command.find("PUT") == 0:

    #  Dosyanın isminin alınması:

    file_title = command[4:]
    allFiles = os.listdir()

    # Dosya varsa:

    if file_title in allFiles:

        file_name = file_title.encode()

        f = open(file_title, "rb")

        data = f.read(bufferSize)

        # Dosya ismi ve dosyanın yollanması

        UDPClientSocket.sendto(file_name, serverAddressPort)
        UDPClientSocket.sendto(data, serverAddressPort)

        while data:
            if UDPClientSocket.sendto(data, serverAddressPort):
                print("Sending...")
                data = f.read(bufferSize)
                time.sleep(0.01)

        try:

            # Timeout bitene kadar bağlantı sağlanmasının beklenmesi

            UDPClientSocket.settimeout(3)
            kontrol = UDPClientSocket.recvfrom(bufferSize)[0].decode()

            if kontrol == "True":  # konsolda bilgilendirme yaptik

                print("File successfully sended.")

        except socket.timeout:

            print("Failed to send file.")

        UDPClientSocket.close()
        f.close()

    else:
        print("Not found.")

else:
    print("Please enter a command which is GET or PUT.")
```


## Çalıştırma

Virtual Box'ta iki tane Ubuntu 20.04 makine kurdum. Bunları aynı NAT üzerinde internete bağlayıp birbirleri ile haberleştiklerinden emin olduktan sonra iki python kodunu da yönteci izinleri ile çalıştırdım. **Eğer port numarası 1023'ten daha çok olursa sudo kullanmanıza gerek kalmayacaktır.**

