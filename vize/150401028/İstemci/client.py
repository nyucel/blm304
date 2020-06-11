#Bartu Utku SARP 150401028

import socket
import time
import os
import sys

try:    #kullanıcı tarafından girilen IP adresi kontrol ediliyor
    socket.gethostbyname(sys.argv[1])
    host = sys.argv[1]
except socket.error:
    print("Hata: Lütfen geçerli bir IP adresi giriniz.")
    sys.exit()
except IndexError:
    print("Sunucu IP adresini giriniz")
    host = input("ftp"+">"+"")

port = 42

try:
    UDPclient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP bağlantısı oluşturuluyor
except:
    print("Bağlantı hatası.")
    sys.exit()

kontrolmsg = 'Kontrol' #sunucu ve istemci arasında kontrol haberleşmeleri 
UDPclient.sendto(kontrolmsg.encode('utf-8'), (host, port))
try:    #kullanıcı tarafında girilen sunucu IP'si ile bir bağlantı oluşturup oluşturulamadığı kontrol ediliyor
    UDPclient.settimeout(3)
    kontrol, server = UDPclient.recvfrom(4096)
except:
    print("Hata: Girdiğiniz server IP adresini ve/veya sunucunuzu kontrol ediniz.")
    sys.exit()

print("Oturum başlatıldı...")
print("-------------------------------------------------------------------------------")

UDPclient.settimeout(7)

baslangicdizinEN, sunucu = UDPclient.recvfrom(4096)
baslangicdizin = baslangicdizinEN.decode('utf8') #başlangıç anında "SunucuDizini" klasöründe bulunan dosyalar
print("Sunucudaki dosyalar", baslangicdizin) #Başlangıçtaki dosyalar kullanıcının işlem yapacağı, sunucu üzerindeki ilgili dizinde bulunan dosyaları görmesi içindir. Herhangi bir işlemden sonra "dir" komutu ile ilgili dizindeki güncel dosyalar yeniden listelenebilir.
print("-------------------------------------------------------------------------------")

istemcidizin = str(os.listdir())
istemcidizini = "İstemciDizini"
#GitHub üzerinden paylaşılan "İstemciDizini" dosyasının indirilmemesi durumunda işlemlerin doğru bir şekilde yapılabildiğini göstermek amacıyla "İstemciDizini" dosyası ve bu dosyanın içine de bir "istemcitest.txt" örnek dosyası oluşturulmuştur
if istemcidizini not in istemcidizin:
    os.mkdir(istemcidizini)
    kontrol = 1
    print("İstemci dizini oluşturuldu.")
    print("-------------------------------------------------------------------------------")
os.chdir(istemcidizini)
if (kontrol == 1):
    testi = open("istemcitest.txt", "w")
    testi.write("Bu dosya istemcide bulunan bir test dosyasıdır.")
    testi.close()
istemcidizin = str(os.listdir())

istemcidir = str(os.getcwd()) #"İstemciDizini" klasörünün dosya yolu
paths, server = UDPclient.recvfrom(4096) 
paths = paths.decode("utf8") #"ServerDizini" klasörünün dosya yolu

while True:
    print("Örnek Kullanım; \nSunucudan Dosya İndirmek İçin; GET dosya_adı\nSunucuya Dosya Yüklemek İçin; PUT dosya_adı\nSunucu Dizinini Listelemek İçin; dir\nBağlantıyı Sonlandırmak İçin; exit")
    print("-------------------------------------------------------------------------------\n")
    komutc = str(input("ftp"+">")) #kullanıcıdan alınan komut
    komutc = komutc.lower() 
    komutEN = komutc.encode('utf-8')
    UDPclient.sendto(komutEN, (host, port)) #kullanıcı tarafından girilen komut sunucuya gönderiliyor
    gkomut = komutc.split()
    if (gkomut[0] == "get"): #sunucudan istemciye dosya indirme
        
        kontrol = "OK" #sunucu ve istemci arasında kontrol haberleşmeleri
        kontrolEN = kontrol.encode('utf-8')
        UDPclient.sendto(kontrolEN, (host, port))
        dosya, sunucuip = UDPclient.recvfrom(4096)
        kontrolmesaj = dosya.decode('utf8')

        if kontrolmesaj == "Dosya bulundu.":
            print(kontrolmesaj)
            print("-------------------------------------------------------------------------------")
            gdosya = open(gkomut[1], "wb") #istemcide bulunan "İstemciDizini" klasörünün içine, indirilmek istenen dosya ile aynı adda bir dosya oluşuturuluyor
            dosyaboyutu, dosyaadresi = UDPclient.recvfrom(4096)
            toplamboyut = dosyaboyutu.decode('utf8')
            toplamboyut = int(toplamboyut)
            
            kontrolboyut, cIP = UDPclient.recvfrom(4096) 
            idboyut1 = kontrolboyut.decode('utf8') #indirme işlemi sonrası dosyanın tamamının gelip gelmediğini kontrol etmek için tanımlanmıştır
            print ("İndirme başlıyor...")
            while toplamboyut != 0:
                try:
                    indirilen, idosyaadres = UDPclient.recvfrom(4096)
                except OSError:
                    print("Hata: Bağlantınızı kontrol ediniz.\nDosya aktarımı kesintiye uğradı.")
                    sys.exit()
                except:
                    print("Hata: Dosya aktarımı bağlantısını kontrol edin.")
                    sys.exit()
                gdosya.write(indirilen)
                print("Aktarımın tamamlanmasına",toplamboyut,"paket kaldı.")
                toplamboyut -= 1
            gdosya.close()
            
            idboyut2 = str(os.stat(istemcidir+"/"+gkomut[1]).st_size) #indirme işlemi sonrası dosyanın tamamının gelip gelmediğini kontrol etmek için tanımlanmıştır
            
            if (idboyut1 == idboyut2):
                print("-------------------------------------------------------------------------------")
                print("Dosya başarıyla indirildi.")
                print("-------------------------------------------------------------------------------")
                okmsj = "OK"
                okmsj = str(okmsj)
                okEN = okmsj.encode('utf-8')
                UDPclient.sendto(okEN, sunucuip)
            else:
                print("Dosya aktarımı kesintiye uğradı.")
                sys.exit()
        else:
            print("Dosya bulunamadı.")
            print("-------------------------------------------------------------------------------")

    elif (gkomut[0] == "put"): #sunucuya dosya yükleme
        ydosya, sunucuip = UDPclient.recvfrom(4096) #sunucu ve istemci arasında kontrol haberleşmeleri

        if os.path.isfile(gkomut[1]): #sunucuya yüklenmesi istenen dosyanın istemcide bulunup bulunmadığının kontrolü
            kontrolmsj = "Dosya bulundu." 
            kontrolmsjEN=kontrolmsj.encode('utf-8')
            UDPclient.sendto(kontrolmsjEN, sunucuip)
            print("Dosya bulundu.")
            print("-------------------------------------------------------------------------------")
            
            dosyab = os.stat(gkomut[1])
            ydosyaboyut = dosyab.st_size
            ydosyaboyutstr = str(ydosyaboyut)
            boyutEN = ydosyaboyutstr.encode('utf-8')
            UDPclient.sendto(boyutEN, sunucuip)    
            spaket = int(ydosyaboyut / 4096)
            spaket += 1
            gpaket = str(spaket)
            paketEN = gpaket.encode('utf8')
            UDPclient.sendto(paketEN, sunucuip)
            isayac = int(spaket)

            ydosya = open(gkomut[1], "rb") #sunucuya yüklenecek dosya okunuyor
            print("Yükleme başlıyor...")
            print("-------------------------------------------------------------------------------")
            while isayac != 0:
                pdosya = ydosya.read(4096)
                try:
                    UDPclient.sendto(pdosya, sunucuip)
                    time.sleep(0.002)
                except OSError:
                    print("Hata: Bağlantınızı kontrol ediniz.\nDosya aktarımı kesintiye uğradı.")
                    sys.exit()
                except:
                    print("Hata: Dosya aktarımı zaman aşımına uğradı. ")
                    sys.exit()
                isayac -= 1

            ydosya.close()

            testmsj, address = UDPclient.recvfrom(4096)
            transfertest = testmsj.decode('utf8')
            if (transfertest == "OK"):
                print("Dosya başarıyla gönderildi.")
                print("-------------------------------------------------------------------------------")
            else:
                print("Hata: Dosya aktarımı kesintiye uğradı.")
                sys.exit()
        else:
            hata = "Dosya bulunamadı"
            hataEN = hata.encode('utf-8')
            UDPclient.sendto(hataEN, sunucuip)
            print("Hata: Dosya bulunamadı.")

    elif (gkomut[0] == "dir"):
        print("-------------------------------------------------------------------------------")
        print("Listelenen dizin: " + str(paths))
        print("-------------------------------------------------------------------------------")
        kontrolmsj, sunucuadres = UDPclient.recvfrom(51200)

        kontrol1 = kontrolmsj.decode('utf8')

        if kontrol1 == "Komut kabul edildi.":
            dizinliste, dizinadres = UDPclient.recvfrom(4096)
            kontrol2 = dizinliste.decode('utf8')
            print(kontrol2)
            print("-------------------------------------------------------------------------------")

    elif (gkomut[0] == "exit"):
        print("-------------------------------------------------------------------------------")
        print("Bağlantınız sonlandırılmıştır.")
        sys.exit()

    else:
        print("-------------------------------------------------------------------------------")
        print("Hata: Lütfen geçerli bir komut giriniz.")
        print("-------------------------------------------------------------------------------")
