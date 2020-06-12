
#Beyza ÇOBAN
#170401012

from scapy.all import*
import os
import time


def ls(destination_ip):

    print("\n")		
    udp_packet = IP( dst = destination_ip ) / UDP( sport = 34, dport = 42 ) / Raw( load = "1" ) 
    send(udp_packet)       #Yapılan secim bilgisi sunucuya bildirildi		
    print("\n")
		
    dosya = sniff( count = 1, filter = "udp port 34", iface = "lo" )   #Sunucuda bulunan dosyaları yakaladık
    print("\nSunucuda Bulunan Dosyaların Listesi\n")
    print( dosya[0].load.decode() )
			
    print("\n")



   	
def get(destination_ip):

        print("\n")              
        udp_packet = IP( dst = destination_ip) / UDP(sport = 34, dport = 42) / Raw(load = "2")
        send(udp_packet)           #Yapılan secim sunucuya bildirildi
        time.sleep(1)
		
        dosya_Adı= input ( "\nGet işlemi yapılacak dosyanın adını giriniz:\n" )
        udp_packet = IP( dst = destination_ip) / UDP(sport = 34, dport = 42) / Raw(load = dosya_Adı)
        send(udp_packet)          #GET yapılacak dosyanın adı iletildi

        dosya = sniff( count = 1, filter = "udp port 34", iface = "lo" )
        check = ( dosya[0].load.decode() )    #GET Islemi yapilacak dosyanın varlığı kontrol edildi
			
			
        if check == "1":           #Get islemi yapilacak dosya sunucuda varsa
				
            dosya2 = sniff( count = 1, filter = "udp port 34", iface = "lo" )
            istemci_veri = dosya2[0].load     #Dosyanın içeriği yakalandı
				
            add = open( dosya_Adı,"wb" )
            add.write( istemci_veri )     #Dosyanın içeriği kaydedildi
            add.close()
			
            print("\nGET işlemi BAŞARILI")
				
				
        if check == "0":    #Get islemi yapilacak dosya sunucuda yoksa
        
            print("\nGET işlemi BAŞARISIZ. Dosya bulunamadı")	
            print("\n")
            
            
            
def put(destination_ip):

    dosya_Adı= input( "\nPut işlemi yapılacak dosyanın adını giriniz: \n" )
	
    if os.path.exists(dosya_Adı) == True:         #PUT Islemi yapilacak dosya istemcide varsa
				
				
        print("\n")
        udp_packet = IP( dst = destination_ip ) / UDP( sport = 34, dport = 42 ) / Raw( load = "3" )
        send(udp_packet)      #Yapılan secim sunucuya iletildi
        time.sleep(1)
		
        udp_packet = IP( dst = destination_ip ) / UDP( sport = 34, dport = 42 ) / Raw( load = dosya_Adı)
        send(udp_packet)      #Dosyanin adi sunucuya iletildi
		
        gonder = open(dosya_Adı,"rb")
        istemci_veri = gonder.read()      #Dosyanin icerigi okundu ve kaydedildi
        gonder.close()
			
        time.sleep(1)
        udp_packet = IP( dst = destination_ip) / UDP(sport = 34, dport = 42) / Raw(load = istemci_veri)
        send(udp_packet)              #Dosyanin iceriği sunucuya iletildi
				
				
        print("\nPUT işlemi BAŞARILI!! Dosya sunucuya iletildi")
			
		
    else:           #PUT Islemi yapilacak dosya istemcide yoksa
			
        print("\nDosya bulunamadı")
        udp_packet = IP( dst = destination_ip) / UDP(sport = 34, dport = 42) / Raw(load = "0")
        send(udp_packet)     #Dosyanin bulunmadığı bildirildi
        time.sleep(1)
				
        print("\n")
        
        

def exit(destination_ip):

        print("\n")              
        udp_packet = IP( dst = destination_ip ) / UDP( sport = 34, dport = 42 ) / Raw( load = "4" )
        send( udp_packet )     #Yapılan secim sunucuya iletildi
			
        print("\nÇıkış Yapıldı\n")
       



os.chdir("istemci_veri")          

destination_ip = input("Baglantı kurulacak Server'in IP numarasini giriniz: \n")      



while True:
	
    print("\nSEÇENEKLER\n1-LİSTELE\n2-GET\n3-PUT\n4-EXIT\n")
    secim = input("Yapmak istediğiniz işlemi seçiniz:")
	
	
    if secim == "1":      # Listele yapılmak istenirse 
		
        print(ls(destination_ip))
			
    elif secim == "2":    #GET işlemi yapılmak istenirse
			
        print(get(destination_ip))
			
    elif secim == "3":    #PUT işlemi yapılmak istenirse
        print(put(destination_ip))	
        
		
    elif secim == "4":     #ÇIKIŞ
			
        print(exit(destination_ip))
        break;	

		
    else :    
        print("\nBAŞARISIZ!! Yanlış seçim yaptınız\n")   
	









