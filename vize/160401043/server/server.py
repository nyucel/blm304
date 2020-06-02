



# HAZIRLAYAN
# ERENAY TOSUN - 160401043



from scapy.all import*
import os
import time


interface_bilgisi = input("\nInterface bilgisini giriniz: ")     #Interface bilgisi alindi....

os.chdir("dosyalar")     #Server Klasoru icerisinde yer alan islem yapacagımız "dosyalar" klasorune yukseldik...



while True: 

	
	secenek = sniff( count = 1, filter = "udp port 42", iface = interface_bilgisi )   #Client tarafindan gonderilen islem numarasi yakalandi...
	register = secenek[0].load.decode()                            #Client'dan gelen seçim register.'a kaydedildi...
	
	client_ip_bilgisi = secenek[0][IP].src                #Bağlantı kurulan Client'ın IP adresi kaydedildi...
	#client_sport = secenek[0].sport                       #gelen port bilgisi
	
	
	if register == "1":                  # Listeleme işlemi seçilme durumu
	
		print("\n")
			
		time.sleep(1)
		udp_packet = IP( dst = client_ip_bilgisi ) / UDP( sport = 42, dport = 35 ) / Raw( load = "\n".join( os.listdir() ) )
		send( udp_packet )           #Server Klasorunun icerisinde bulunan "dosyalar"  klasorunde yer alan dosyaların listesi Client'a gonderildi...
		
		print( "\nListeleme Işlemi Tamamlandı...\n\n" )
		
	
	
	elif register == "2":                  #PUT işlemi seçilme durumu
	
		print("\n")
		dosya = sniff(count = 1, filter = "udp port 42", iface = interface_bilgisi)
		file_name = dosya[0].load.decode()     #Gelen dosyanın adı kaydedildi...
		
		
		dosya2 = sniff(count = 1, filter = "udp port 42", iface = interface_bilgisi)
		veri = dosya2[0].load            #Gelen dosyanın içeriği kaydedildi...
		
		add = open( file_name,"wb" )       #Client tarafindan gonderilen dosya, Server Klasoru icerisinde bulunan dosyalar klasorune eklendi...
		add.write( veri )
		add.close()
		
		print( "\n PUT Islemi Tamamlandi...\n" )
		
			
			
	elif register == "3":	   		#GET işlemi seçilme durumu
	
	
		print("\n")
		dosya = sniff(count = 1, filter = "udp port 42", iface = interface_bilgisi)
		file_name = dosya[0].load          #Gelen dosyanın adı kaydedildi...
		
		
		if os.path.exists(file_name) == True:       #Client tarafından Get işlemi yapılmak istenilen dosyanın Server'da var olup olmama kontrol edildi...
			
			
			time.sleep(1)
			udp_packet = IP(dst = client_ip_bilgisi) / UDP(sport = 42, dport = 35) / Raw(load = "1")
			send(udp_packet)                   #Dosyanin bulundugunu bildirme amacli kontrol degeri olarak Client'e 1 degeri gonderildi... 
			
			
			gonder = open(file_name,"rb")      #Get islemi yapılacak dosyanın icindeki veriler okundu ve kaydedildi...
			veri = gonder.read()
			gonder.close()
			
			
			
			time.sleep(1)
			udp_packet = IP( dst = client_ip_bilgisi) / UDP(sport = 42, dport = 35) / Raw(load = veri)
			send(udp_packet)                  #Get islemi yapılacak olan dosyanın icerigi Client'e gonderildi...
			
			print("\nGET Islemi Tamamlandi...\n")
	
			
		elif os.path.exists(file_name) == False:
		
			time.sleep(1)
			udp_packet = IP( dst = client_ip_bilgisi) / UDP(sport = 42, dport = 35) / Raw(load = "2")
			send(udp_packet)
			print("\nGET Islemi Basarisiz...\n")
	
		
	
	
	elif register == "4":                   #Programı sonlandirma durumu
		
		print("\n...Server Durduruldu...Program Sonlandırıldı...\n")
		break;
		
		
		
		
		
		
		
		
