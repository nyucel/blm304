#170401070 - Başak KILIÇ

from scapy.all import*
import os
import time

def listeleme(d_ip):
	print("\n")	
	
	time.sleep(1)	#Sunucu dosyaları liste halinde istemciye gönderilir.
	paket = IP( dst = d_ip ) / UDP( sport = 42, dport = 38 ) / Raw( load = "\n".join( os.listdir()))
	send(paket)    
	     
	print("Listeleme işlemi gerçekleştirildi.")	

def get(d_ip,dosya_adi):		
	dosya = open(dosya_adi,"rb")
	if(dosya.read() == b''):	#Dosya içeriği boşsa sunucu istemciyi BOS ile bilgilendirir.
		dosya.close()
		time.sleep(1) 
		paket = IP( dst = d_ip ) / UDP( sport = 42, dport = 38 ) / Raw( load = "BOS")
		send(paket)  

	else:			#Dosya içeriği doluysa sunucu istemciyi DOLU ile bilgilendirir ve dosya içeriğini gönderir.
		time.sleep(1) 
		paket = IP( dst = d_ip ) / UDP( sport = 42, dport = 38 ) / Raw( load = "DOLU")
		send(paket)  
		
		dosya = open(dosya_adi,"rb")
		dosya_icerik = dosya.read()
		dosya.close()
		
		time.sleep(1) 
		paket = IP( dst = d_ip ) / UDP( sport = 42, dport = 38 ) / Raw( load = dosya_icerik)
		send(paket)  		
	
	print("İstemciye ekleme işlemi gerçekleştirildi. ")
		
def put():
	dosya = sniff( count = 1, filter = "udp port 42", iface = "lo")
	dosya_adi = dosya[0].load
	
	kontrol = sniff( count = 1, filter = "udp port 38", iface = "lo" ) #İstemci dosyasında içeriğinin olup olmadığı yakalanır.
	test = kontrol[0].load.decode()
	if(test =="BOS"):		#Boşsa yeni bir dosya oluşturulur.
		dosya = open(dosya_adi,"wb")
		dosya.close()
	else: 	#Doluysa yeni bir dosya oluşturulup içerik eklenir.

		dosya_icerik = sniff( count = 1, filter = "udp port 42", iface = "lo")
		icerik = dosya_icerik[0].load
		
		dosya = open(dosya_adi,"wb")
		dosya.write(icerik)
		dosya.close()
	
	print("Sunucuya ekleme işlemi gerçekleştirildi. ")

		
os.chdir("sunucu_Klasor") 	#sunucu.py nin bulunduğu dizindedir.
   
paket = sniff( count = 1, filter = "udp port 42", iface = "lo")  
istek = paket[0].load.decode()

d_ip = paket[0][IP].src  #istemci ip	

while True: 
	listeleme(d_ip)

	komut = sniff( count = 1, filter = "udp port 42", iface = "lo") #Gelen komut yakalanır.
	komut_ismi = komut[0].load.decode()
	
	if(komut_ismi == "GET"):
		dosya = sniff( count = 1, filter = "udp port 42", iface = "lo")
		dosya_adi = dosya[0].load
		
		 #Sunucuda dosyanın bulunup bulunmadığı bilgisi istemciye gönderilir.
		if os.path.exists(dosya_adi) == True: 
			time.sleep(1)   	
			paket = IP( dst = d_ip ) / UDP( sport = 42, dport = 38 ) / Raw( load = "true")
			send(paket)  
			
			get(d_ip,dosya_adi)	#Bulunuyorsa ekleme işlemi gerçekleştirilir.
		else:
			print("İlgili dosya sunucuda bulunamadı. ")
			
			time.sleep(1)	
			paket = IP( dst = d_ip ) / UDP( sport = 42, dport = 38 ) / Raw( load = "false")
			send(paket) 
			
	elif(komut_ismi == "PUT"):
		dosya_kontrolu = sniff( count = 1, filter = "udp port 38", iface = "lo" )
		test = dosya_kontrolu[0].load.decode()
		
		if(test == "true"):	#İstemcide dosya mevcutsa put işlemini gerçekleştirir.
			put()
		else:	
			print("İlgili dosya istemcide bulunamadı. ")
			
	elif(komut_ismi == '0'):
		print("İstemci Tarafından sonlandırıldı")
		break
		
	else:
		print("\nGeçersiz komut girişi yapıldı.")


		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		



