#sunucu (server)

import socket, time , os, sys

#Bircan ARSLAN 170401013


IP = str(socket.gethostbyname(socket.gethostname()+".local"))            #Sunucunun başlatılıdığı bilgisayarın IP bilgisini otomatik olarak alma
port = 42


try:
    
    UDP_connect = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDP_connect.bind((IP, port))                                         #IP ve port bağlantısı kuruldu
except:
    print("Hata! Sunucu başlatılamadı.")
    sys.exit()

print("Sunucu IP Adresi: ", IP)
print(port,"numaralı port dinleniyor...")

buffers = 4096

try:

    firtcom, istemcia = UDP_connect.recvfrom(buffers)
except:
    print("Hata! Bağlantı kurulamadı.") 
    sys.exit()    

sendip = str(IP)
sendip_encode = sendip.encode('utf-8')
UDP_connect.sendto(sendip_encode, istemcia)
serverdir=str(os.listdir())
checkdir = "SunucuDiziniDosyaları"

if checkdir in serverdir:

    os.chdir(checkdir)
    usedir = str(os.listdir())
else:
    usedir = str(os.listdir())

usedir_encode = usedir.encode('utf-8')
UDP_connect.sendto(usedir_encode, istemcia)
serverpath=str(os.getcwd())
serverpath_encode=serverpath.encode("utf-8")
UDP_connect.sendto(serverpath_encode, istemcia)

def Get(targetfile):
    test, clienta = UDP_connect.recvfrom(buffers)
    test1=1
    try:
        
        tfile = open(targetfile, "rb")                                  #Kullanıcı tarafından indirilecek dosya "rb" komutu ile okunuyor
    except FileNotFoundError:
        kontrol = "Nope!"
        kontrolEN = kontrol.encode('utf-8')
        UDP_connect.sendto(kontrolEN, clienta)
        print("Hata! İstenen dosya sunucu dizininde bulunamadı.")
        test1=0
     
    if (test1 != 0):
        kontrol = "Selam!"
        kontrolEN = kontrol.encode('utf-8')
        UDP_connect.sendto(kontrolEN, clienta)                          #İndirme işleminin başlatılması için sunucuya bir mesaj gönderilmesi gerekiyor
        print("İstenen dosya sunucu dizininde bulundu. İndirme başlıyor...")
  
        filesize = os.stat(targetfile).st_size                          #Dosya boyutunun alınması

        packetnum = int(filesize / 4096) + 1                            #Dosyanın paketlere bölünmesi
        packetstr = str(packetnum)
        packetstr_encode = packetstr.encode('utf-8')
        UDP_connect.sendto(packetstr_encode, clienta)  
        sizestr = str(filesize)
        sizestr_encode = sizestr.encode('utf-8') 
        UDP_connect.sendto(sizestr_encode, clienta)                     #İndirme işlemi sonrası indirilen dosyayı kontrol etmek amacıyla başlangıçtaki dosya boyutunu gönderiyoruz
        count = int(packetnum)
        for i in range(count,0,-1):
            rfile = tfile.read(buffers)                                 #İndirilecek dosyanın okunması
            try:

                UDP_connect.sendto(rfile, clienta)
            except OSError:
                print("Hata! İnternet bağlantınızı kontrol ediniz.")
                sys.exit()
            except:
                print("Hata! Zaman aşımı.")
                sys.exit()
            time.sleep(0.005)                                           #Gönderilen paket arasında bir süre bekleniyor

        tfile.close()

        checkmsg, clienta = UDP_connect.recvfrom(buffers)
        mesaj = checkmsg.decode('utf-8')
        if (mesaj == "Tamam!"):                                         #İstemciden gelen onay mesajı
            print("İstenen dosya başarıyla gönderildi.")
        else:
            print("Hata! İstenen dosya gönderilirken paket kaybı yaşandı.")
            sys.exit()
        
def Put():
    kontrol = "Selam!"
    kontrol_encode = kontrol.encode('utf-8')
    UDP_connect.sendto(kontrol_encode, clienta)
    
    kontrolmsj, kontrola = UDP_connect.recvfrom(buffers)
    mesaj = kontrolmsj.decode('utf-8')

    if mesaj == "Tamam!":
        sdosyaboyutu, dosyaadresi = UDP_connect.recvfrom(buffers)       #Dosya boyutu istemciden alındı
        kontrol1 = sdosyaboyutu.decode('utf-8')                         #Yükleme işlemi sonrası yüklenen dosyayı kontrol etmek amacıyla kullanıyoruz
        UDP_connect.settimeout(10)
        hedefdosya = open(isteksp[1], "wb")                             #Kullanıcı tarafından yüklenen dosya ile aynı isimde bir dosya sunucu üzerinde oluşturuluyor
        print("Dosya bulundu. Yükleme başlıyor...")
        packet, packetaddr = UDP_connect.recvfrom(buffers)
        sayac = packet.decode('utf-8')
        sayac = int(sayac)
        for j in range(sayac,0,-1):
            try:

                serverfile, sunucuadresi = UDP_connect.recvfrom(buffers)
            except OSError:
                print("Hata! Bağlantınızı kontrol ediniz.")
                sys.exit()
            except:
                print("Hata! Dosya aktarımı zaman aşımına uğradı. ")
                sys.exit()
            hedefdosya.write(serverfile)                                #Yüklenmek istenen dosya içeriği sunucuda oluşturduğumuz dosyaya yazılıyor
            sayac -= 1
        hedefdosya.close()

        kontrol2 = str(os.stat(serverpath + "/" + isteksp[1]).st_size)  #Yükleme işlemi sonrası yüklenen dosyayı kontrol etmek amacıyla kullanıyoruz
        if (kontrol1 == kontrol2):                                      #Dosya boyutları karşılaştırıldı        
            print("İstenen dosya sunucuya başarıyla yüklendi.")
            test2 = "Kontrol!"
            test2str = str(test2)
            test2str_encode = test2str.encode('utf-8')
            UDP_connect.sendto(test2str_encode, clienta)
        else:
            print("Hata! İstenen dosya sunucuya yüklenirken kesintiye uğradı.")
            sys.exit()
    else:
        print("Hata! Dosya yüklenemedi.")

def List():
    print("Sunucu dizininde bulunan dosyalar listeleniyor...")
    kontrol = "Geçerli komut."
    kontrol_encode = kontrol.encode('utf-8')
    UDP_connect.sendto(kontrol_encode, clienta)
    pathdir = os.listdir(serverpath)
    pathdirstr = str(pathdir)
    pathdirstr_encode = pathdirstr.encode('utf-8')
    UDP_connect.sendto(pathdirstr_encode, clienta)

def Cikis():
    print("Bağlantınız sonlandırılmıştır.")
    sys.exit()   

while True:
    UDP_connect.settimeout(1000)    
    try:

        istek, clienta = UDP_connect.recvfrom(buffers)                  #İstemciden komutun alınması
    except socket.timeout:
        print("Hata! Bağlantı zaman aşımına uğradı. Lütfen yeniden bağlanın.")
        sys.exit()
    isteksptr = istek.decode('utf-8')
    isteksp = isteksptr.split()                                         #İstemciden alınan komut ve dosya adının ayrıştırılması
    if (isteksp[0] == "get"):
        Get(isteksp[1])
    elif (isteksp[0] == "put"):
        Put()
    elif (isteksp[0] == "list"):
        List()
    elif (isteksp[0] == "q"):
        Cikis()
    else:
        print("Hata! Lütfen geçerli bir komut giriniz.")
