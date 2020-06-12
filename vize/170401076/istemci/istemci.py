# Onur Karabulut - 170401076
import socket
import time
import sys
import os
import select

sct = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
size = 32768
port = 42


def file_control(file_name):
    if file_name[:4] == "PUT ":
        lst = os.listdir(os.getcwd()+"/istemci_dosyalari")
        for i in lst:
            if file_name[4:] == i:
                return True
    elif file_name == "CIKIS" or file_name[:4] == "GET ":
        return True
    print("Hatalı Komut veya Dosya Adı")
    return False


def put_file(choose):
    flname = choose.encode("utf-8")
    sct.sendto(flname, (ip, port))
    f = open("istemci_dosyalari/" + choose[4:], "rb")
    file_size = os.stat("istemci_dosyalari/" + choose[4:])[6]
    file_size_send = str(file_size).encode("utf-8")
    sct.sendto(file_size_send, (ip, port))
    file_data = f.read(size)
    size_control = 1
    print("Dosya Sunucuya Aktarılıyor..")
    while file_data:
        sct.sendto(file_data, way)
        file_data = f.read(size)
        size_control += 1
        time.sleep(0.2)
    if size*size_control >= file_size:
        f.close()
        print("Dosya Başarıyla Sunucuya Aktarıldı")

    cmd_control = False
    while cmd_control == False:
        print("İşlemlere Devam İçin: 1, Programı Sonlandırmak İçin: 2 Giriniz")
        devam = str(input("İşleminiz: "))
        if devam == '1':
            return None
        elif devam == '2':
            print("Program Sonlanıyor..")
            sys.exit()
        else:
            print("Hatalı Giriş !!!")


def get_file(choose):
    file_name = choose.encode("utf-8")
    sct.sendto(file_name, (ip, port))
    data, way = sct.recvfrom(size)
    file_control = data.decode("utf-8")
    if file_control == "True":
        file_size_data, way = sct.recvfrom(size)
        file_size = int(file_size_data.decode("utf-8"))
        f = open("istemci_dosyalari/" + choose[4:].strip(), 'wb')
        size_control = 0
        print("Dosya Sunucudan Alınıyor")
        while True:
            readable = select.select([sct], [], [], 0.5)
            if readable[0]:
                file_data, adres = sct.recvfrom(size)
                f.write(file_data)
                size_control += 1
            if file_size <= (size_control * size):
                f.close()
                print("Dosya Başarıyla Sunucudan Alındı")
                break

    else:
        print("Girilen Dosya Sunucuda Yok !!!")

    cmd_control = False
    while cmd_control == False:
        print("İşlemlere Devam İçin: 1, Programı Sonlandırmak İçin: 2 Giriniz")
        devam = str(input("İşleminiz: "))
        if devam == '1':
            return None
        elif devam == '2':
            print("Program Sonlanıyor..")
            sys.exit()
        else:
            print("Hatalı Tuşlama Yaptınız")



print("Server IP Adresini Giriniz")
ip = str(input("IP: "))
conMsg = "connection".encode("utf-8")
while True:
    sct.sendto(conMsg, (ip, port))
    try:
        data, way = sct.recvfrom(size)
    except:
        print("Bağlanılmak İstenen Sunucu Aktif Değil, Program Sonlanıyor")
        sys.exit()
    fileList = data.decode("utf-8")
    print(fileList)
    file_cnt = False
    while file_cnt == False:
        print("Komutunuzu Giriniz")
        print("GET dosya_adi.tip, PUT dosya_adi.tip veya CIKIS")
        operation = str(input("Komutunuz: "))
        file_cnt = file_control(operation)
        if file_cnt == True:
            if operation[:4] == "GET ":
                get_file(operation)
            elif operation[:4] == "PUT ":
                put_file(operation)
            elif operation == "CIKIS":
                print("Program Sonlandırılıyor..")
                sys.exit()







