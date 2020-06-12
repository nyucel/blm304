#Bartu Utku SARP 150401028

import socket
import time
import os
import sys

serverIP = str(socket.gethostbyname(socket.gethostname()+".local")) #sunucunun mevcut interface'ine ait IP adresi otomatik alınıyor
port = 42

try: #UDP bağlantısının başarılı bir şekilde oluşuturulup oluşturulamadığı kontrol ediliyor
    UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDP.bind((serverIP, port))
except:
    print("Hata: Bağlantı hatası.") 
    sys.exit()

print("Server IP Adresi: ", serverIP) #otomatik alınan IP adresi, istemciye kullanıcı tarafından girilmesi için ekrana yazdırılıyor
print("-------------------------------------------------------------------------------")
print(port,"numaralı port dinleniyor. İstemci bekleniyor...")
print("-------------------------------------------------------------------------------")

try:
    kontroli, clientIP = UDP.recvfrom(4096) #sunucu ve istemci arasında kontrol haberleşmeleri
except:
    print("Hata: Bağlantı hatası.") 
    sys.exit()    

kontrol = str(serverIP)
kontrolEN = kontrol.encode('utf-8')
UDP.sendto(kontrolEN, clientIP)

bdizin=str(os.listdir())
sunucudizini = "SunucuDizini"
#GitHub üzerinden paylaşılan "SunucuDizini" dosyasının indirilmemesi durumunda, işlemlerin doğru bir şekilde yapılabildiğini göstermek amacıyla "SunucuDizini" dosyası ve bu dosyanın içine de bir "sunucutest.txt" örnek dosyası oluşturulmuştur
if sunucudizini not in bdizin:
    os.mkdir(sunucudizini)
    kontrol = 1
    print("Sunucu dizini oluşturuldu.")
    print("-------------------------------------------------------------------------------")
os.chdir(sunucudizini)
if (kontrol == 1):
    test = open("sunucutest.txt", "w")
    test.write("Bu dosya sunucuda bulunan bir test dosyasıdır.")
    test.close()
bdizin=str(os.listdir())
bdizinEN = bdizin.encode('utf-8')
UDP.sendto(bdizinEN, clientIP) #başlangıç anında "SunucuDizini" klasöründeki dosyaları ekrana yazdırılmak üzere istemciye gönderiyor

path=str(os.getcwd()) #"SunucuDizini" klasörünün dosya yolu bulunuyor
pathEN=path.encode("utf-8")
UDP.sendto(pathEN, clientIP) #"SunucuDizini" klasörünün bulunduğu dosya yolu istemciye gönderiliyor

def Listeleme(): #dir komutu
    print("Bu servis için ayrılmış dizin dosyaları listeleniyor...")
    print("-------------------------------------------------------------------------------")
    kontrol = "Komut kabul edildi." #dosyaların listelenmesi için istemciye gönderilen onay mesajı
    kontrolEN = kontrol.encode('utf-8')
    UDP.sendto(kontrolEN, istemciadres)

    liste = os.listdir(path)
    listestr = str(liste)
    listeEN = listestr.encode('utf-8')
    UDP.sendto(listeEN, istemciadres)

def Download(sunucudosya): #GET komutu
    kontrol1, istemciadres = UDP.recvfrom(4096)
    kontrolc=1
    try:    #istemci tarafından indirilmek istenen dosyanın sunucuda bulunup bulunmadığının kontrolü 
        dosya = open(sunucudosya, "rb") #istemci tarafından indirilecek dosya okunuyor
    except FileNotFoundError:
        kontrol = "Dosya bulunamadı."
        kontrolEN = kontrol.encode('utf-8')
        UDP.sendto(kontrolEN, istemciadres)
        print("Dosya bulunamadı.")
        print("-------------------------------------------------------------------------------")
        kontrolc=0
     
    if (kontrolc != 0):
        kontrol = "Dosya bulundu." #istenen dosya sunucuda bulunduğunda indirme işleminin başlatılması için bir onay mesajı gönderiliyor
        kontrolEN = kontrol.encode('utf-8')
        UDP.sendto(kontrolEN, istemciadres)
        print("Dosya bulundu.")
        print("-------------------------------------------------------------------------------")
    
        boyutS = os.stat(sunucudosya) #dosya bilgilerine erişim
        boyut = boyutS.st_size #dosya boyutunu okumak

        paket = int(boyut / 4096) #paket sayısı
        paket += 1
        paketstr = str(paket)
        paketEN = paketstr.encode('utf-8')
        UDP.sendto(paketEN, istemciadres)
    
    
        boyutstr = str(boyut)
        boyutEN = boyutstr.encode('utf-8')
        UDP.sendto(boyutEN, istemciadres)
    
        toplamboyut = int(paket)
        print("İndirme başlıyor...")
        print("-------------------------------------------------------------------------------")
        while toplamboyut != 0:
            idosya = dosya.read(4096)
            try:
                UDP.sendto(idosya, istemciadres)
            except OSError:
                print("Hata: Bağlantınızı kontrol ediniz.\nDosya aktarımı kesintiye uğradı.")
                sys.exit()
            except:
                print("Hata: Dosya aktarımı zaman aşımına uğradı. ")
                sys.exit()
            time.sleep(0.002) #dosya gönderiminde sorun yaşamamak için istemcinin gönderilen dosyaları yazması bekleniyor
            toplamboyut -= 1

        dosya.close()

        kontrolmsj, istemciadres = UDP.recvfrom(4096)
        test = kontrolmsj.decode('utf8')
        if (test == "OK"):
            print("Dosya başarıyla gönderildi.")
            print("-------------------------------------------------------------------------------")
        else:
            print("Hata: Dosya aktarımı kesintiye uğradı.")
            sys.exit()
        
def Upload(): #PUT komutu
    kontrol = "OK" #sunucu ve istemci arasında kontrol haberleşmeleri
    kontrolEN = kontrol.encode('utf-8')
    UDP.sendto(kontrolEN, istemciadres)
    
    kontrolmesaj, kontroladresi = UDP.recvfrom(4096)
    mesaj = kontrolmesaj.decode('utf8')

    if mesaj == "Dosya bulundu.":
        print("Dosya bulundu.")
        print("-------------------------------------------------------------------------------")
        gdosyaboyutu, dosyaadres = UDP.recvfrom(4096)
        dosyaboyutu1 = gdosyaboyutu.decode('utf8') #yükleme işlemi sonrası dosyanın tamamının gelip gelmediğini kontrol etmek için tanımlanmıştır
        UDP.settimeout(7)
        gelendosya = open(bkomut[1], "wb") #sunucuda "SunucuDizini" klasörüne, yüklenmek istenen dosya ile aynı adda bir dosya oluşuturuluyor
        
        gpaket, gdosyaadres = UDP.recvfrom(4096)
        sayac = gpaket.decode('utf8')
        sayac = int(sayac)
        while sayac !=0 :
            try:
                sunucudosya, sunucuadres = UDP.recvfrom(4096)
            except OSError:
                print("Hata: Bağlantınızı kontrol ediniz.")
                sys.exit()
            except:
                print("Hata: Dosya aktarımı zaman aşımına uğradı. ")
                sys.exit()
            gelendosya.write(sunucudosya)
            print("Aktarımın tamamlanmasına",sayac,"paket kaldı")
            sayac -= 1

        gelendosya.close()

        dosyaboyutu2 = str(os.stat(path + "/" + bkomut[1]).st_size) #yükleme işlemi sonrası dosyanın tamamının gelip gelmediğini kontrol etme için tanımlanmıştır
        if (dosyaboyutu1 == dosyaboyutu2):     
            print("-------------------------------------------------------------------------------")
            print("Dosya başarıyla sunucuya yüklendi.")
            print("-------------------------------------------------------------------------------")
            testmsj = "OK"
            testmsj = str(testmsj)
            testEN = testmsj.encode('utf-8')
            UDP.sendto(testEN, istemciadres)
        else:
            print("Dosya aktarımı kesintiye uğradı.")
            sys.exit()
    else:
        print("Dosya yüklemesi başarısız.")
        print("-------------------------------------------------------------------------------")
def Bitir():
    print("Bağlantınız sonlandırılmıştır.")
    sys.exit()   

while True:
    UDP.settimeout(4242)    
    try:
        komut, istemciadres = UDP.recvfrom(4096) #kullanıcı tarafından girilen komut
    except socket.timeout:
        print("Bağlantı zaman aşımına uğradı. Lütfen yeniden bağlanın.")
        sys.exit()
    komutstr = komut.decode('utf8')
    bkomut = komutstr.split()
    if bkomut[0] == "get":
        Download(bkomut[1])
    elif bkomut[0] == "put":
        Upload()
    elif bkomut[0] == "dir":
        Listeleme()
    elif bkomut[0] == "exit":
        Bitir()
    else:
        print("-------------------------------------------------------------------------------")
        print("Hata: Lütfen geçerli bir komut giriniz.")
        print("-------------------------------------------------------------------------------")
