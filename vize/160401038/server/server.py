
from scapy.all import*
import os
import time


#--------Şamil GÜVEN 160401038-----------


interfaceInfo = input("Interface bilgisini giriniz : ")     #Interface bilgisi aliniyor
os.chdir("serverFiles")

while True: 

	choice = sniff( count = 1, filter = "udp port 42", iface = interfaceInfo )   #Client tarafindan gelen islem numarasi aliniyor.
	choosen = choice[0].load.decode()                            #Client'dan gelen seçim choosen'a kaydediliyor.
	clientIpInfo = choice[0][IP].src                #Bağlantı yapilan Client'ın IP adresi kaydediliyor.
	
	if choosen == "1":
	
		print("\n")
			
		time.sleep(1)
		udpPacket = IP( dst = clientIpInfo ) / UDP( sport = 42, dport = 16 ) / Raw( load = "\n".join( os.listdir() ) )
		send( udpPacket )           #Server Klasorunde bulunan "serverFiles"  klasorunde yer alan dosyaların listesi Client'a gonderiliyor

	elif choosen == "2":

		print("\n")
		file = sniff(count=1, filter="udp port 42", iface=interfaceInfo)
		fileName = file[0].load  # Gelen dosyanın adi kaydediliyor.

		if os.path.exists(fileName) == True:  # Client tarafından Get işlemi yapılmak istenilen dosyanın Server'da  olup olmadiği kontrol ediliyor

			time.sleep(1)
			udpPacket = IP(dst=clientIpInfo) / UDP(sport=42, dport=16) / Raw(load="1")
			send(
				udpPacket)  # Dosyanin var oldugunu bildirmek amaciyla kontrol degeri olarak Client'e 1 degeri gonderiliyor

			sendFile = open(fileName, "rb")  # Get islemi yapılacak olan  dosyanın icindeki veriler okundu ve kaydedildi
			data = sendFile.read()
			sendFile.close()

			time.sleep(1)
			udpPacket = IP(dst=clientIpInfo) / UDP(sport=42, dport=16) / Raw(load=data)
			send(udpPacket)  # Get islemi yapılacak dosyanın icerigi Client'e gonderiliyor


		elif os.path.exists(fileName) == False:

			time.sleep(1)
			udpPacket = IP(dst=clientIpInfo) / UDP(sport=42, dport=16) / Raw(load="2")
			send(udpPacket)

	elif choosen == "3":

		print("\n")
		file = sniff(count=1, filter="udp port 42", iface=interfaceInfo)
		fileName = file[0].load.decode()  # Gelen dosyanın adı kaydediliyor

		file2 = sniff(count=1, filter="udp port 42", iface=interfaceInfo)
		data = file2[0].load  # Gelen dosyanın içeriği kaydediliyor

		add = open(fileName,
				   "wb")  # Client tarafindan gonderilen dosya, Server Klasoru icerisinde bulunan serverFiles klasorune ekleniyor
		add.write(data)
		add.close()

	elif choosen == "4":
		
		print("\n-----Program Sonlandirildi----\n")
		break;
		
		
		
		
		
		
		
		
