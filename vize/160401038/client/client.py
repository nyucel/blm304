
from scapy.all import*
import os
import time

#--------Şamil GÜVEN 160401038-----------



os.chdir("clientFiles")
targetIpAdress = input("Baglantı kurulmak istenilen Server'in IP adresini giriniz.\n")      #Bağlantı kurulacak olan  Server'ın IP bilgisi alınır ve kaydedilir


while True:

	print("\nListeleme icin 1`e, GET icin 2`e, PUT icin 3`e , Sonlandirmak icin 4`e basiniz...\n")
	selected = input("Secmek  istediginiz islem numarasini giriniz:  ")

	if selected == "1" or selected == "2" or selected == "3" or selected == "4":
		
		if selected == "1":
		
			print("\n")
			
			udpPacket = IP( dst = targetIpAdress ) / UDP( sport = 16, dport = 42 ) / Raw( load = "1" ) 
			send(udpPacket)                  #Yapılan secim  Server'a gonderiliyor
			
			print("\n")
		
			file = sniff( count = 1, filter = "udp port 16", iface = "lo" )   #Serverda yer alan dosyalarin listesi aliniyor
			print("\n<--Serverda yer alan dosyalar-->\n")
			print( file[0].load.decode() )
			
			print("\n\n")
			
		elif selected == "2":

			print("\n")
			udpPacket = IP(dst=targetIpAdress) / UDP(sport=16, dport=42) / Raw(load="2")
			send(udpPacket)  # Yapılan secim Server'a gonderiliyor
			time.sleep(1)

			fileName = input("\nGet işlemi yapılmasini istediginiz dosyanın adını giriniz: \n")
			udpPacket = IP(dst=targetIpAdress) / UDP(sport=16, dport=42) / Raw(load=fileName)
			send(udpPacket)  # GET islemi yapilacak dosyanin adi Server'a gonderiliyor

			file = sniff(count=1, filter="udp port 16", iface="lo")
			control = (
				file[0].load.decode())  # GET islemi yapilacak dosyanin var olup olmadiginin kontrol bilgisi aliniyor

			if control == "1":  # Get islemi yapilacak dosya Server'da mevcutsa

				file2 = sniff(count=1, filter="udp port 16", iface="lo")
				data = file2[0].load  # Get islemi yapilacak dosyanin icerigi alindi

				add = open(fileName, "wb")
				add.write(data)  # Get islemi yapilacak dosyanin icerigi kaydedildi
				add.close()

				print("\nGET işlemi yapilmistir.dosya Server'dan alindi")

			if control == "2":  # Get islemi yapilacak dosya Server'da mevcut degilse.

				print("\nGET işlemi basarisiz olmustur. Server'da boyle bir dosya bulunamamistir.")

			print("\n")

		elif selected == "3":

			fileName = input("\n Put islemi yapilmasini istediginiz dosyanın adını giriniz: \n")

			if os.path.exists(fileName) == True:

				print("\n")
				udpPacket = IP(dst=targetIpAdress) / UDP(sport=16, dport=42) / Raw(load="3")
				send(udpPacket)  # Yapılan secim  Server'a gonderiliyor
				time.sleep(1)

				udpPacket = IP(dst=targetIpAdress) / UDP(sport=16, dport=42) / Raw(load=fileName)
				send(udpPacket)  # PUT islemi yapilacak dosyanin adi Server'a gonderiliyor

				sendFile = open(fileName, "rb")
				data = sendFile.read()  # PUT islemi yapilacak dosyanin icerigi okundu ve kaydedildi
				sendFile.close()

				time.sleep(1)
				udpPacket = IP(dst=targetIpAdress) / UDP(sport=16, dport=42) / Raw(load=data)
				send(udpPacket)  # PUT Islemi yapilacak dosyanin icerigi Server'a gonderiliyor

				print("\nPUT islemi yapilmistir.Dosya basariyla Server'a gonderildi.")

			else:  # PUT islemi yapilmasi istenilen dosya Client'da mevcut degilse

				print("\nBu isimde bir dosya bulunamadı.")
				udpPacket = IP(dst=targetIpAdress) / UDP(sport=16, dport=42) / Raw(load="5")
				send(udpPacket)  # Dosyanin mevcut olmamasi halinde bir kontrol degeri gonderiliyor.
				time.sleep(1)

			print("\n\n")

		elif selected == "4":
			
			
			print("\n")              
			udpPacket = IP( dst = targetIpAdress) / UDP(sport = 16, dport = 42) / Raw(load = "4")
			send(udpPacket)        #Yapılan secim Server'a gönderiliyor
			time.sleep(1)
			
			print("\n<--Program Sonlandirildi-->\n")
			break;	
		
		
			
	else:
	
		print("\nGeçersiz işlem girdiniz. Tekrar deneyiniz.\n")
	









