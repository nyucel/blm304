import socket
import os


##########
#İBRAHİM KAÇMAZ
# NO: 150401078
##########


s=socket.socket()
host=input(str("lütfen sunucunun host adresini giriniz:"))
port=42
s.connect((host,port))

print("bağlandı...")

#######
# SUNUCUDAKİ KLASÖRLER EKRANA YAZILIR
folder_path=r'C:\Users\Asus X550V\PycharmProjects\haberlesme_odev'
filenames=os.listdir(folder_path)
for filename in filenames:
    print("SUNUCUDAKİ DOSYA ADI:"+filename)
#######
islem=input(str("sunucudan dosya indirmek için get,sunucuya dosya yüklemek için put değeri giriniz..."))
if islem=="get":
    filename = input(str("Lütfen gelen dosya için bir dosya adı girin:"))
    file = open("new_"+filename, 'wb')#dosyay açar
    file_data = s.recv(1024)
    file.write(file_data)
    file.close()

if islem=="put":

    s = socket.socket()
    host = socket.gethostname()
    port = 42
    s.bind((host, port))
    s.listen(1)
    print(host)
    print("Gelen bağlantılar bekleniyor...")
    conn, addr = s.accept()
    print(addr)
    print("sunucuya bağlandı")
    filename = input(str("Lütfen gönderilecek dosyanın adını giriniz:"))
    if os.path.exists(filename) == True:
        print("dosya mevcut")
        file = open(filename, 'rb')
        file_data = file.read(1024)
        conn.send(file_data)
        print("bilgiler gönderildi")
    else:
        yeni = input(str("böyle bir dosya yok,yeniden denemek ister misiniz? y/n"))
        if yeni == 'y':
            islem = input(str("sunucudan dosya indirmek için get,sunucuya dosya yüklemek için put değeri giriniz..."))
            if islem == "get":
                filename = input(str("Lütfen gelen dosya için bir dosya adı girin:"))
                file = open("new_" + filename, 'wb')  # dosyay açar
                file_data = s.recv(1024)
                file.write(file_data)
                file.close()

            if islem == "put":


                filename = input(str("Lütfen gönderilecek dosyanın adını giriniz:"))
                if os.path.exists(filename) == True:
                    print("dosya mevcut")
                    file = open(filename, 'rb')
                    file_data = file.read(1024)
                    conn.send(file_data)
                    print("bilgiler gönderildi")
        if yeni == 'n':
            print("programdan çıkılıyor.")







    s.close()
