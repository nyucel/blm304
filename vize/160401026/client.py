#160401026 -- Kerim ULUSOY

import socket
import os

soket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sunucu_ip = input('ip giriniz:', end =" " )
sunucu_address = (sunucu_ip, 42)
while True:
    print('1 - get')
    print('2 - put')
    print('3 - listele')
    p = input("request :", end=" ")

    if p == "1":
        dosya_adi = input('dosya_adi :', end =" ")
        sent = soket.sendto(("get:"+dosya_adi).encode(), sunucu_address)
        f = open(dosya_adi,'wb')
        data,addr = soket.recvfrom(1024)
        try:
            while(data):
                if data.find("--ENDFILE--".encode()) == -1:
                    f.write(data)
                else:
                    f.write(data[:data.find("--ENDFILE--".encode())])
                    f.close()
                    soket.settimeout(999999)
                    break
                soket.settimeout(2)
                data,addr = soket.recvfrom(1024)
        except socket.timeout:
            soket.settimeout(999999)
            f.close()
            if data.find("--ENDFILE--".encode()) == -1:
                print("Hata!")
        continue
    elif p == "2":
        print('dosya_adi :', end =" ")
        dosya_adi = input()
        if os.path.exists(dosya_adi) == False:
            print("Hata : " + dosya_adi + " bulunamadi!")
            continue
        sent = soket.sendto(("put:"+dosya_adi).encode(), sunucu_address)
        data,addr = soket.recvfrom(1024)
        sent = soket.sendto("continue".encode(), sunucu_address)
        f = open(dosya_adi,"rb")
        data = f.read(1024)
        while (data):
            if(soket.sendto(data, sunucu_address)):
                data = f.read(1024)
        soket.sendto("--ENDFILE--".encode(), sunucu_address)
        f.close()
        continue
    elif p == "3":
        sent = soket.sendto("list".encode(), sunucu_address)
        data, server = soket.recvfrom(4096)
        print('\ndosya listesi : \n%s' % data.decode())
    else:
        continue
