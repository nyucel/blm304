



# HAZIRLAYAN
# ERENAY TOSUN - 160401043



from scapy.all import*
import os
import time


#print(os.getcwd())
os.chdir("veriler")            #Client Klasoru icerisinde yer alan islem yapacagımız "veriler" klasorune yukseldik...

hedef_ip_adresi = input("\nBaglantı kurulmak istenilen Server'in IP numarasini giriniz...\n")      #Bağlantı kurulacak Server'ın IP bilgisi alındı ve kaydedildi...



while True:
	
	

	print("\n------------MENU--------------\n1-Listeleme\n2-PUT\n3-GET\n4-Cikis\n")
	register = input("Istenilen islem numarasini giriniz:  ")
	# Yapilabilecek islemler icin bir menu olusturuldu ve istenilen islemin numarasi kaydedildi...
	
	
	
	if register == "1" or register == "2" or register == "3" or register == "4":
	
	
	
		if register == "1":      # Listeleme işlemi seçilme durumu
		
			print("\n")
			
			udp_packet = IP( dst = hedef_ip_adresi ) / UDP( sport = 35, dport = 42 ) / Raw( load = "1" ) 
			send(udp_packet)                  #Yapılan secim bilgisi Server'a iletildi...
			
			print("\n")
			
			
			dosya = sniff( count = 1, filter = "udp port 35", iface = "lo" )   #Serverda yer alan dosyalarin listesi yakalandi...
			print("\n-----SERVERDA BULUNAN DOSYALAR-----\n")
			print( dosya[0].load.decode() )
			
			print("\n\n")
			
		
			
		elif register == "2":        #PUT işlemi seçilme durumu
			
			
			
			file_name = input( "\nPut() işlemi yapılması istenen dosyanın adını giriniz: \n" )
			
			
			
			if os.path.exists(file_name) == True:             #PUT Islemi yapilmasi istenilen dosyanin Client'da mevcut ise...
				
				
				print("\n")
				udp_packet = IP( dst = hedef_ip_adresi ) / UDP( sport = 35, dport = 42 ) / Raw( load = "2" )
				send(udp_packet)               #Yapılan secim bilgisi Server'a iletildi...
				time.sleep(1)
				
				
				udp_packet = IP( dst = hedef_ip_adresi ) / UDP( sport = 35, dport = 42 ) / Raw( load = file_name )
				send(udp_packet)               #PUT Islemi yapilacak dosyanin adi Server'a iletildi...
				
				
				gonder = open(file_name,"rb")
				veri = gonder.read()            #PUT Islemi yapilacak dosyanin icerigi okundu ve kaydedildi...
				gonder.close()
				
				
				time.sleep(1)
				udp_packet = IP( dst = hedef_ip_adresi) / UDP(sport = 35, dport = 42) / Raw(load = veri)
				send(udp_packet)              #PUT Islemi yapilacak dosyanin icerigi Server'a iletildi...
				
				
				print("\nPUT işlemi tamamlanmıştır...Dosya başarıyla Server'a iletildi...")
			
			
			
			else:                               #PUT Islemi yapilmasi istenilen dosyanin Client'da mevcut degil ise...
			
				print("\nBu isimde bir Dosya bulunamadı...")
				udp_packet = IP( dst = hedef_ip_adresi) / UDP(sport = 35, dport = 42) / Raw(load = "5")
				send(udp_packet)           #Dosyanin mevcut olmamasi halinde bir kontrol degeri gonderildi...
				time.sleep(1)
				
				
			print("\n\n")
			
	
	
			
		elif register == "3":         #GET işlemi seçilme durumu
		
		
			print("\n")              
			udp_packet = IP( dst = hedef_ip_adresi) / UDP(sport = 35, dport = 42) / Raw(load = "3")
			send(udp_packet)             #Yapılan secim bilgisi Server'a iletildi...
			time.sleep(1)
			
			
			file_name = input ( "\nGet() işlemi yapılması istenen dosyanın adını giriniz: \n" )
			udp_packet = IP( dst = hedef_ip_adresi) / UDP(sport = 35, dport = 42) / Raw(load = file_name)
			send(udp_packet)             #GET Islemi yapilacak dosyanin adi Server'a iletildi...
			
			
			dosya = sniff( count = 1, filter = "udp port 35", iface = "lo" )
			control = ( dosya[0].load.decode() )      #GET Islemi yapilacak dosyanin var olup olmadiginin kontrol bilgisi yakalandi...
			
			
			if control == "1":           #Get islemi yapilacak dosya Server'da mevcut ise...
				
				
				dosya2 = sniff( count = 1, filter = "udp port 35", iface = "lo" )
				veri = dosya2[0].load      #Get islemi yapilacak dosyanin icerigi yakalandi...
				
				
				add = open( file_name,"wb" )
				add.write( veri )            #Get islemi yapilacak dosyanin icerigi kaydedildi...
				add.close()
				
				print("\nGET işlemi tamamlanmıştır...Dosya Server'dan alındı...")
				
				
			if control == "2":         #Get islemi yapilacak dosya Server'da mevcut degil ise...
			
			
				print("\nGET işlemi BAŞARISIZ...Server'da Boyle bir dosya bulunamadı...")
				
			
	
			print("\n\n")
		
		
		
		elif register == "4":            #Programi sonlandirma durumu
			
			
			print("\n")              
			udp_packet = IP( dst = hedef_ip_adresi ) / UDP( sport = 35, dport = 42 ) / Raw( load = "4" )
			send( udp_packet )        #Yapılan secim bilgisi Server'a iletildi...
			time.sleep(1)
			
			print("\n...Program Sonlandirildi...\n")
			break;	
		
		
			
	else:           #Menude olmayan bir durum secildiginde verilen uyari...
	
		print("\nGeçersiz işlem numarası girdiniz... Tekrar deneyiniz...\n\n")   
	









