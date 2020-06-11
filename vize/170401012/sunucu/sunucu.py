
#Beyza ÇOBAN-170401012


from scapy.all import*
import os
import time


def ls(client_ip_bilgisi):
    
    print("\n")
    time.sleep(1)
    udp_packet = IP( dst = client_ip_bilgisi ) / UDP( sport = 42, dport = 34) / Raw( load = "\n".join( os.listdir() ) )
    send( udp_packet )        #Sunucu klasorunun icerisinde bulunan sunucu_veri klasorundeki dosyaların listesi istemciye gonderildi
		
    print( "\nDosyalar Listelendi\n" )
		
	

def get(interface_desc, client_ip_bilgisi ):

    print("\n")
    dosya = sniff(count = 1, filter = "udp port 42", iface = interface_desc)
    dosya_Adı = dosya[0].load     #Get yapılacak dosyanın adı kaydedildi    
		
    if os.path.exists(dosya_Adı) == True:    #Dosya sunucuda varsa
		
        time.sleep(1)
        udp_packet = IP(dst = client_ip_bilgisi) / UDP(sport = 42, dport = 34) / Raw(load = "1")
        send(udp_packet)                   
	
        gonder = open(dosya_Adı,"rb")   #dosyanın icindeki veriler okundu ve kaydedildi
        istemci_veri = gonder.read()
        gonder.close()
		
        time.sleep(1)
        udp_packet = IP( dst = client_ip_bilgisi) / UDP(sport = 42, dport = 34) / Raw(load = istemci_veri)
        send(udp_packet)       #dosyanın icerigi istemciye gönderildi         
			
        print("\nGET Islemi BAŞARILI\n")
	
			
    elif os.path.exists(dosya_Adı) == False:  # Dosya sunucuda yoksa
		
        time.sleep(1)
        udp_packet = IP( dst = client_ip_bilgisi) / UDP(sport = 42, dport = 34) / Raw(load = "0")
        send(udp_packet)
        print("\nGET Islemi BAŞARISIZ\n")
        


def put(interface_desc):

    print("\n")
    dosya = sniff(count = 1, filter = "udp port 42", iface = interface_desc)
    dosya_Adı = dosya[0].load.decode()   #Put yapılacak dosyanın adı kaydedildi
	
    dosya2 = sniff(count = 1, filter = "udp port 42", iface = interface_desc)
    istemci_veri = dosya2[0].load   #Dosyanın içeriği kaydedildi      
		
    add = open( dosya_Adı,"wb" )  #istemciden gönderilen dosya server_veri klasorune eklendi
    add.write( istemci_veri )
    add.close()
		
    print( "\n PUT Islemi BAŞARILI\n" )

		
		
interface_desc = input("Interface bilgisini giriniz: ")     

os.chdir("sunucu_veri")     


while True: 

    secenek = sniff( count = 1, filter = "udp port 42", iface = interface_desc )   
    secim = secenek[0].load.decode()                          
	
    client_ip_bilgisi = secenek[0][IP].src   #istemci ip bilgisi alındı             
	
		
    if secim == "1":          #Sunucudaki dosyaları listeleme işlemi seçilirse
	
        print(ls(client_ip_bilgisi))
		
	
    elif secim == "2":         #PUT işlemi seçilirse
	
        print(get(interface_desc,client_ip_bilgisi))
        
			
    elif secim == "3":	   	#GET işlemi seçilirse
	
        print(put(interface_desc))
		
	
    elif secim == "4":         #Programdan çıkış yapılmak istenirse
        print("\nÇıkış Yapıldı\n")
        break;
		
 	
		
		
		
		
		
		
		
