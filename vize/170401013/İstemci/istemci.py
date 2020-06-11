#istemci (client)

import socket, time , os, sys

#Hazırlayan: Bircan ARSLAN 170401013

try:    

    socket.gethostbyname(sys.argv[1])
    istemciIP = sys.argv[1]
except socket.error:
    print("Hata! Bağlanacağınız sunucunun IP adresini giriniz: ")
    sys.exit()
except IndexError:
    istemciIP = input("Bağlanacağınız sunucunun IP adresini giriniz: ")

port = 42
buffers = 4096
bbuffers = 51200

try:
    UDP_connect = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      #istemci bağlantısı oluşturuluyor
except:
    print("Hata! İstemci başlatılamadı.")
    sys.exit()

start_comm = 'Selam!' 
UDP_connect.sendto(start_comm.encode(), (istemciIP, port))
try:    

    UDP_connect.settimeout(5)
    kontrol, server = UDP_connect.recvfrom(buffers)
except:
    print("Hata! Bağlantı kurulamadı.")
    sys.exit()

print("Oturum başlatıldı.")

UDP_connect.settimeout(10)
firstlist, adres1 = UDP_connect.recvfrom(buffers)
ilkdizin = firstlist.decode()

print("Sunucu dizinindeki dosyalar:", ilkdizin)                        #Bağlantı kurulduktan sonra kullanılabilecek dosyaların listesi

kontroldizin = str(os.listdir())
targetdir = "İstemciDiziniDosyaları"                                   #İşlemlerin yapıldığı klasör

if targetdir in kontroldizin:
    os.chdir(targetdir)
    dizindir = str(os.listdir())
else:
    dizindir = str(os.listdir())

clientdir = str(os.getcwd())                                           #İstemci.py dosyasının konumu
clientpath1, adres2 = UDP_connect.recvfrom(buffers) 
clientpath = clientpath1.decode("utf8")                                #Sunucu.py dosyasının konumu

while True:
    print("╔════════════════════════════════════════════════════════╗")
    print("║Komutların Örnek Kullanımları:                          ║")
    print("║GET dosya_adı                                           ║")
    print("║PUT dosya_adı                                           ║")
    print("║list                                                    ║")
    print("║Çıkış:q                                                 ║")
    print("╚════════════════════════════════════════════════════════╝")
    
    girilen_komut = str(input("$ftp"+">"))                            #Komutların alındığı kısım
    girilen_komut = girilen_komut.lower()
    girilen_komut_encode = girilen_komut.encode()
    UDP_connect.sendto(girilen_komut_encode, (istemciIP, port))       #Kullanıcı tarafından girilen komutların sunucuya aktarımı
    komut_kontrol = girilen_komut.split()                             #Komutların ayrıştırılması

    if (komut_kontrol[0] == "get"):
        
        iletisimtest = "Selam!"
        iletisimtest_encode = iletisimtest.encode('utf-8')
        UDP_connect.sendto(iletisimtest_encode, (istemciIP, port))
        indirilecek_dosya, adres3 = UDP_connect.recvfrom(buffers)
        testmesaj = indirilecek_dosya.decode('utf-8')

        if testmesaj == "Selam!":
          
            hedef_dosya = open(komut_kontrol[1], "wb")                #İstemci üzerinde indirilmek istenen dosya ile aynı adda bir dosya oluşturulması
            hedefboyut1, hedefadres = UDP_connect.recvfrom(buffers)
            hedefboyut = hedefboyut1.decode('utf-8')
            targetint = int(hedefboyut)
            checksize, checkIP = UDP_connect.recvfrom(buffers) 
            size1 = checksize.decode('utf-8')                         #İndirme işlemi sonrası dosyanın kontrolü için kullanılacaktır
            
            print("Belirtilen dosya sunucu dizininde bulundu. İndirme başlıyor...")
            
            for i in range(targetint,0,-1):
                try:

                    downfile, adres4 = UDP_connect.recvfrom(buffers)
                except OSError:
                    print("Hata! Bağlantı hatası.")
                    sys.exit()
                except:
                    print("Hata! Aktarım tamamlanamadı.")
                    sys.exit()
                hedef_dosya.write(downfile)                            #İndirilen dosya içeriğinin sunucu üzerinde oluşturuduğumuz dosyaya yazılması

            hedef_dosya.close()
            size2=str(os.stat(clientdir+"/"+komut_kontrol[1]).st_size) #İndirme işlemi sonrası dosyanın kontrolü için kullanılacaktır
            if (size1 == size2):                                       #Dosya boyutlarının karşılaştırılması
                
                print("İstenen dosyanın indirilmesi paket kaybı yaşanmadan tamamlandı.")
                
                onaymsg = "Tamam!"
                onaymsgstr = str(onaymsg)
                onaymsgstr_encode = onaymsgstr.encode('utf-8')
                UDP_connect.sendto(onaymsgstr_encode, hedefadres)
            else:
                print("İstenen dosyanın indirilmesi sırasında bağlantı hatası nedeniyle paket kaybı yaşandı.")
                sys.exit()
        else:
            print("Hata! Sunucu dizininde hedef dosya bulunamadı.")

    elif (komut_kontrol[0] == "put"):
        uploadfile, serveraddr = UDP_connect.recvfrom(buffers)
        test3 = 1
        try:

            targetfile = open(komut_kontrol[1], "rb")
        except:
            checkmsg = "Nope!"
            msg_encode = checkmsg.encode('utf-8')
            UDP_connect.sendto(msg_encode, serveraddr)
            print("Hata! Belirtilen dosya istemci dizininde bulunamadı.")
            test3 = 0
        if(test3 != 0):    
            kontrolmsj = "Tamam!" 
            kontrolmsj_encode=kontrolmsj.encode('utf-8')
            UDP_connect.sendto(kontrolmsj_encode, serveraddr)
            print("Belirtilen dosya istemci dizininde bulundu. Dosya gönderimi başlıyor...")
        
            target_file_size = int(os.stat(komut_kontrol[1]).st_size)
            sizestr = str(target_file_size)
            sizestr_encode = sizestr.encode('utf-8')
            UDP_connect.sendto(sizestr_encode, serveraddr)    
            packetnum = int(target_file_size / 4096) + 1
            packetstr = str(packetnum)
            packet_encode = packetstr.encode('utf-8')
            UDP_connect.sendto(packet_encode, serveraddr)
            upload_count = int(packetnum)
        
            for j in range(upload_count,0,-1):
                wfile = targetfile.read(buffers)
                try:
                    UDP_connect.sendto(wfile, serveraddr)
                    time.sleep(0.005)
                except OSError:
                    print("Hata! Bağlantı hatası.")
                    sys.exit()
                except:
                    print("Hata! Aktarım tamamlanamadı.")
                    sys.exit()

            targetfile.close()

            testmsj, address = UDP_connect.recvfrom(buffers)
            transfertest = testmsj.decode()
            if (transfertest == "Kontrol!"):                         #Yükleme kayıp yaşanmadan tamamlandı kontrolü
                print("İstenen dosyanın yüklemesi paket kaybı yaşanmadan tamamlandı.")
            
            else:
                print("İstenen dosyanın yüklenmesi sırasında bağlantı hatası nedeniyle paket kaybı yaşandı.")
                sys.exit()

    elif (komut_kontrol[0] == "list"):
        
        print("Dosya yolu: " + str(clientpath))                      #Dosya yolu yazdırma
        
        checkcomm, serceraddr = UDP_connect.recvfrom(bbuffers)
        check = checkcomm.decode()

        if check == "Geçerli komut.":
            listdir, diraddr = UDP_connect.recvfrom(buffers)
            checki = listdir.decode()

            print(checki)
            

    elif (komut_kontrol[0] == "q"):
        
        print("Bağlantınız sonlandırılmıştır.")
        sys.exit()        
    else:
        print("Hata! Lütfen geçerli bir komut giriniz.")
