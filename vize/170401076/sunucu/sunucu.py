# Onur Karabulut - 170401076
import socket
import os
import select
import time


sct = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
IP = ""
port = 42
size = 32768


def files():
    a = os.listdir(os.getcwd()+"/sunucu_dosyalari")
    b = "---SERVER DOSYALARI---"
    for i in range(len(a)):
        b += "\n {0} - {1}".format(i+1, str(a[i]))
    return b


def put_data(order):
    f = open("sunucu_dosyalari/" + order[4:], 'wb')
    file_size_data, way = sct.recvfrom(size)
    file_size = int(file_size_data.decode("utf-8"))
    print("{0} Dosyası {1} IP'li İstemciden Alınıyor".format(order[4:], way[0]))
    size_control = 0
    while True:
        readable = select.select([sct], [], [], 0.5)
        if readable[0]:
            file_data, way2 = sct.recvfrom(size)
            f.write(file_data)
            size_control += 1
        if file_size <= (size_control * size):
            f.close()
            print("{0} Dosyası {1} IP'li İstemciden Başarıyla Alındı".format(order[4:], way[0]))
            break


def get_file(order, way):
    file_list = os.listdir(os.getcwd()+"/sunucu_dosyalari")
    file_control = 0
    for i in file_list:
        if order[4:] == i:
            file_msg = "True".encode("utf-8")
            sct.sendto(file_msg, way)
            file_size = os.stat("sunucu_dosyalari/" + order[4:])[6]
            file_size_send = str(file_size).encode("utf-8")
            sct.sendto(file_size_send, way)
            f = open("sunucu_dosyalari/"+order[4:], "rb")
            size_control = 1
            file_data = f.read(size)
            print("{0} Dosyası {1} IP'li İstemciye Yollanıyor".format(order[4:], way[0]))
            while file_data:
                sct.sendto(file_data, way)
                file_data = f.read(size)
                size_control += 1
                time.sleep(0.2)
            if size * size_control >= file_size:
                f.close()
                print("{0} Dosyası  {1} IP'li İstemciye Başarıyla Yollandı".format(order[4:], way[0]))
            break
        else:
            file_control += 1
        if file_control == len(file_list):
            file_msg = "False".encode("utf-8")
            sct.sendto(file_msg, way)



sct.bind((IP,port))
while True:
    connect_data, way = sct.recvfrom(size)
    if connect_data and way:
        cnnt = connect_data.decode("utf-8")
        if cnnt == "connection":
            msg = files().encode("utf-8")
            print("{0} IP'li İstemci Sunucuya Bağlandı ".format(way[0]))
            sct.sendto(msg, way)
            order_data, way = sct.recvfrom(size)
            order = order_data.decode("utf-8")
            if order[:4] == "GET ":
                get_file(order, way)
            elif order[:4] == "PUT ":
                put_data(order)







                
                    


        

