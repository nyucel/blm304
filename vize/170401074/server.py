import time
import socket
import os

IP = ""#str(socket.gethostbyname(socket.gethostname() + ".local"))
port   = 42
#print("IP Adresi >>", IP)
buffer  = 65000

def main():
    while(True): 
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.bind((IP, port))             
        m, address = s.recvfrom(buffer)    
        mesaj = m.decode('utf-8')

        if(mesaj == "listele"):
            print("Yapilacak islem >> Listeleme")
            sozluk = []
            for i in os.listdir(os.getcwd()):
                sozluk.append(i)
            if(not sozluk):
                print("Server dosyasi bos...")
            x = str(len(sozluk))
            s.sendto(x.encode(), address)
            for i in range(len(sozluk)):
                s.sendto(str.encode(sozluk[i]), address)
            
        if(mesaj == "kapat"):
            print("Server-Client baglantisi kapandi. Program kapaniyor...")
            s.close()
            exit(1)       
            
        if(mesaj == "put"):
            print("Yapilacak islem >> PUT")
            dosya_adi = s.recvfrom(buffer)#gelen dosya adi
            dosya_boyutu = s.recvfrom(buffer)#gelen dosyanin boyutu
            dosya_adi = dosya_adi[0].decode() 
            dosya_boyutu = dosya_boyutu[0].decode()
            dosya_boyutu = int(dosya_boyutu)
            print("Gelen dosyanin adi >>",dosya_adi)
            print("Gelen dosyanin boyutu >>",dosya_boyutu , "byte")
            f = open(dosya_adi, "wb")
            data, adres = s.recvfrom(buffer)
            try:
                print("Dosya aliniyor...")
                while(data):
                    s.settimeout(0.05)
                    time.sleep(0.05)
                    f.write(data)
                    data, adres = s.recvfrom(buffer)
            except:
                f.close()
                time.sleep(0.5)
                s.settimeout(0.5)
                ff =  os.stat(dosya_adi)
                sonraki_boyut = ff.st_size
                if(sonraki_boyut < int(dosya_boyutu)):#gelen dosya boyutu mesaji ile server dosyasina gonderilen dosya boyutunu karsilastiriyoruz
                    print("Dosya eksik sekilde alindi ya da hic alinmadi")
                    s.sendto(str.encode("basarisiz"), address)
                else:
                    print("Dosya basariyla alindi :D ")
                    s.sendto(str.encode("basarili"), address)                
        if(mesaj == "get"):
            sozluk = []
            for i in os.listdir(os.getcwd()):
                sozluk.append(i)
            if(not sozluk):
                print("Server dosyasi bos...")
            x = str(len(sozluk))
            print("Yapilacak islem >> GET")
            dosya_adi = s.recvfrom(buffer) 
            dosya_adi = dosya_adi[0].decode()
            print("Dosya adi >>",dosya_adi)

            if(dosya_adi not in sozluk):
                s.sendto(str.encode("dosyayok"), address)
                print("Dosya server klasorunde yok...")
            elif(dosya_adi in sozluk):                
                s.sendto(str.encode("Dosya bulundu.Aktarim basliyor..."), address)
                dosya_adi = dosya_adi.encode()
                s.sendto(dosya_adi, address)
                dosya_boyutu =  os.stat(dosya_adi)     
                dosya_boyutu = dosya_boyutu.st_size
                dosya_boyutu = str(dosya_boyutu)
                db = str.encode(dosya_boyutu)
                s.sendto(db, address)       #dosya boyutunu yolladik                                
                x = os.stat(dosya_adi).st_size
                print("Gonderilen dosya boyutu >>", x)
                f = open(dosya_adi, "rb")
                data = f.read(buffer)
                print("Gonderiliyor...")
                while(data):
                    if(s.sendto(data, address)):
                        s.settimeout(0.05)
                        time.sleep(0.05)
                        data = f.read(buffer)       #dosyayi okuduk
                data = []
                f.close()
                time.sleep(0.5)
                s.settimeout(0.5)
                basarili1 = s.recvfrom(buffer) 
                basarili = basarili1[0].decode()
                if(basarili == "basarili"):
                    print("Dosya basarili sekilde gonderildi")
                elif(basarili == "basarisiz"):
                    print("Dosya eksik sekilde gonderildi ya da gonderilmedi")
                s.close()
        s.close()

def klasor_kontrol():
    konum = os.listdir()
    if("server_dosyalari" not in konum):
        os.mkdir("server_dosyalari")
        os.chdir(os.getcwd() + "//server_dosyalari")   
    elif("server_dosyalari" in konum):
        os.chdir(os.getcwd() + "//server_dosyalari")
        
klasor_kontrol()
print("Batuhan ÖZALP - 170401074 - github.com/bozalp")
while(1):
    main()



    
    
    
    
    
    
    
    
