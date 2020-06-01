import socket
import os

##########
#İBRAHİM KAÇMAZ
# NO: 150401078
##########

s=socket.socket()
host=socket.gethostname()
port=42
s.bind((host,port))
s.listen(1)
print(host)
print("Gelen bağlantılar bekleniyor...")
conn,addr=s.accept()
print(addr)
print("sunucuya bağlandı")

def dosya_yukle():
    os.listdir()
    islem=input(str("sunucuya dosya yüklemek için y, istemciye dosya yüklemek için n seçiniz"))


    if islem=='n':
        filename = input(str("Lütfen istemciye gönderilecek dosyanın adını giriniz:"))
        if os.path.exists(filename) == True:
            print("dosya mevcut")
            file = open(filename, 'rb')
            file_data = file.read(1024)
            conn.send(file_data)
            print("bilgiler gönderildi")
        else:
            yeni = input(str("böyle bir dosya yok,yeniden denemek ister misiniz? y/n"))
            if yeni == 'y':
                dosya_yukle()
            if yeni == 'n':
                print("programdan çıkılıyor.")
                return

    if islem=='y':
        s = socket.socket()
        host = input(str("lütfen istemcinin host adresini giriniz:"))
        if host==" ":
            print("programdan çıkılıyor")
            return
        else:
            port = 42
            s.connect((host, port))
            filename = input(str("Lütfen gelen dosya için bir dosya adı girin:"))
            file = open("new_" + filename, 'wb')
            file_data = s.recv(1024)
            file.write(file_data)
            file.close()



s.close()

dosya_yukle()