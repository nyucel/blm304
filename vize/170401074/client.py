import socket
import os
import time
#Batuhan ÖZALP - 170401074
IP = str(input("IP Adresini Girin >>"))
IPvePort  = (IP, 42)
    
buffer = 65000
def server_dosyalari():
    mesaj = str.encode("listele")   
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.sendto(mesaj, IPvePort)
    
    dosya_sayisi = s.recvfrom(buffer)        
    x = int(dosya_sayisi[0].decode())
    i=0
    if(x == 0):
        print("Server Dosyasi bos...")
    if(x > 0):
        print("\t***Server tarafindaki dosyalar***")
        while(True):
            m2 = s.recvfrom(buffer)        
            print(m2[0].decode())
            if(i >= x - 1):
                break
            i+=1
    menu()
    s.close()
    
def PUT(gonderilecek_dosya):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    yol = os.getcwd()#bulunduğumuz dizin   
    dizi = []
    for i in os.listdir(yol):
        dizi.append(i)
    if(not dizi):
        print("Client klasoru bos...")        
    if(gonderilecek_dosya not in dizi):
        print("Dosya client klasorunde bulunamadi. Dosyanin ya da client klasorunun varligindan emin olun...")
    else:  
        mesaj = str.encode("put")    
        s.sendto(mesaj, IPvePort)
        dosya_boyutu =  os.stat(gonderilecek_dosya)
        print("Secilen dosyanin boyutu -->", dosya_boyutu.st_size, "byte")
        gonderilecek_dosya = gonderilecek_dosya.encode()
        s.sendto(gonderilecek_dosya, IPvePort)                   
        dosya_boyutu = dosya_boyutu.st_size
        dosya_boyutu = str(dosya_boyutu)
        db = str.encode(dosya_boyutu)
        s.sendto(db, IPvePort)
        f = open(gonderilecek_dosya, "rb")
        data = f.read(buffer)
        print("Gonderiliyor...")
        while(data):
            if(s.sendto(data, IPvePort)):                
                time.sleep(0.05)
                s.settimeout(0.05)
                data = f.read(buffer)#dosyayi okuduk             
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
    menu()
    
def GET(gelen_dosya):   
    mesaj = str.encode("get")        
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     
    s.sendto(mesaj, IPvePort) #get gonder
    dosya_adi = str.encode(gelen_dosya)#dosya adini yolladık
    s.sendto(dosya_adi, IPvePort)    
    gelen_mesaj = s.recvfrom(buffer)
    
    if(gelen_mesaj[0].decode() == "dosyayok"):
        print("Server klasorunde belirtilen dosya yok...")
    else:
        dosya_adi = s.recvfrom(buffer)#gelen dosya adi
        dosya_boyutu = s.recvfrom(buffer)#gelen dosyanin boyutu     
        dosya_adi = dosya_adi[0].decode() 
        dosya_boyutu = dosya_boyutu[0].decode()
        dosya_boyutu = int(dosya_boyutu)                    
        yol = os.getcwd()#bulunduğumuz dizin
        print(yol)
        print("Gelen dosyanin adi >>",dosya_adi)
        print("Gelen dosyanin boyutu >>",dosya_boyutu , "byte")
        f = open(dosya_adi, "wb")
        data, adres = s.recvfrom(buffer)
        print("Dosya aliniyor...")
        try:
            while(data):
                time.sleep(0.05)
                f.write(data)
                s.settimeout(0.05)
                data, adres = s.recvfrom(buffer)
        except:
            f.close()
            time.sleep(0.5)
            s.settimeout(0.5)
            ff =  os.stat(dosya_adi)
            sonraki_boyut = ff.st_size
            if(sonraki_boyut < int(dosya_boyutu)):
                print("Dosya eksik sekilde alindi ya da hic alinmadi")
                s.sendto(str.encode("basarisiz"), IPvePort)
            else:
                print("Dosya basariyla alindi :D ")
                s.sendto(str.encode("basarili"), IPvePort)

    menu()
def client_dosyalari():
    print("\t***Client tarafindaki dosyalar***")
    yol = os.getcwd()
    dizi = []
    for i in os.listdir(yol):
        dizi.append(i)
    if(not dizi):
        print("Client klasoru bos...")
    else:
        for i in dizi:
            print(i)
    menu()
 
def kapat(): 
    mesaj = str.encode("kapat")   
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         
    s.sendto(mesaj, IPvePort)
    print("Server-Client baglantisi kapandi. Program kapaniyor...")
    s.close()
    exit(1)
 
def menu():
    print("\t\t***CLIENT MENU***")
    print("Server dosyalarini listelemek için >>LIST SERVER")
    print("Server dosyalarini listelemek için >>LIST CLIENT")
    print("Serverdan dosya indirmek için >>GET dosya_adi.uzanti")
    print("Servera dosya gondermek için >>PUT dosya_adi.uzanti")
    print("Server ve client baglantisini kesmek icin >>CLOSE")
    istek = str(input(">>"))
    if(istek == "LIST SERVER"):
        server_dosyalari()
    elif(istek == "LIST CLIENT"):
        client_dosyalari()
    elif("GET " in istek):
        x = istek.split()
        GET(x[1])
    elif(istek == "CLOSE"):
        kapat()
    elif("PUT " in istek):
        x = istek.split()
        PUT(x[1])
    else:
        print("'%s' gecerli bir komut degil. Lutfen gecerli bir komut girin..." %istek )
        menu()
               
def klasor_kontrol():
    konum = os.listdir()
    if("client_dosyalari" not in konum):
        os.mkdir("client_dosyalari")
        os.chdir(os.getcwd() + "//client_dosyalari")        
    elif("client_dosyalari" in konum):
        os.chdir(os.getcwd() + "//client_dosyalari")
klasor_kontrol()
print("Batuhan ÖZALP - 170401074 - github.com/bozalp")
menu()

    
    
    