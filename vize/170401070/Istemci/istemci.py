#170401070 - Başak KILIÇ

from scapy.all import*
import os
import time

def islem():						#Kullanıcı isteğini komut ve dosya adı olarak parçalar.
	istek = input("Gerçekleştirmek istediğiniz işlem: ")

	if(istek[0:3] == "GET" or istek[0:3] == "PUT"):
		if(istek[3] == " "):
			return (istek[0:3], str(istek[4:len(istek)]))
		else:
			return (istek[0:3], str(istek[3:len(istek)]))		
	elif(istek == '0'):
		return ('0', " ")	
	else:
		return(istek, " ")
	
def listeleme(d_ip):			#Sunucu tarafından gönderilen dosyaları yakalayıp listeler.
	dosya_listesi = sniff( count = 1, filter = "udp port 38", iface = "lo" )

	print("\nSunucuda bulunan dosyalar: \n" + dosya_listesi[0].load.decode() + "\n")

def get(dosya_adi,d_ip):		#İstemciye sunucudan dosya yükler.

	kontrol = sniff( count = 1, filter = "udp port 38", iface = "lo" ) 
	test = kontrol[0].load.decode()
	if(test =="BOS"):			#Dosya içeriği boşsa dosya adını kullanarak yeni bir dosya oluşturur.
		dosya = open(dosya_adi,"wb")
		dosya.close()
	else:	
		dosya = sniff( count = 1, filter = "udp port 38", iface = "lo" )#Dosya doluysa sunucunun gönderdiği içeriği yakalar.
		icerik = dosya[0].load

		dosya = open(dosya_adi,"wb")	#Yeni bir dosya oluşturup içeriği ekler. 
		dosya.write(icerik)
		dosya.close()
	
		
def put(dosya_adi,d_ip):
	paket = IP( dst = d_ip )/ UDP( sport = 38, dport = 42 )/ Raw( load = dosya_adi) #Eklenmek istenen dosya adı sunucuya gönderilir.
	send(paket)
	time.sleep(1)
	
	dosya = open(dosya_adi,"rb")		
	if(dosya.read() == b''):	#Dosya içeriği boşsa BOS bilgisini gönderirir.
		dosya.close()	
		time.sleep(1) 
		paket = IP( dst = d_ip ) / UDP( sport = 42, dport = 38 ) / Raw( load = "BOS")
		send(paket)  
	else:				#Dosya içeriği doluysa DOLU bilgisini ve dosya içeriği gönderirir.
		time.sleep(1) 
		paket = IP( dst = d_ip ) / UDP( sport = 42, dport = 38 ) / Raw( load = "DOLU")
		send(paket)  
			
		dosya = open(dosya_adi,"rb")
		dosya_icerik = dosya.read()
		dosya.close()
		
		time.sleep(1)
		paket = IP( dst = d_ip )/ UDP( sport = 38, dport = 42 )/ Raw( load = dosya_icerik)
		send(paket)
	

	
os.chdir("istemci_Klasor")           		#istemci.py nin bulunduğu dizindedir.

d_ip= input("\nSunucunun IP adresini giriniz: ") 
print("\nSunucudan dosya getirmek için: GET dosyaAdi ")
print("Sunucuya dosyayı yüklemek için: PUT dosyaAdi")
print("Çıkış yapmak için: 0 \n")

gonderilen_paket = IP( dst = d_ip )/ UDP( sport = 38, dport = 42 )/ Raw( load = "packet" )
send(gonderilen_paket)  

while True:
	listeleme(d_ip)
	(komut,dosya_adi) = islem()
	#Hangi komut olursa olsun komut bilgisi sunucuya iletilir.
	
	if(komut == "GET" or komut == "PUT"):
		paket = IP( dst = d_ip )/ UDP( sport = 38, dport = 42 )/ Raw( load = komut)
		send(paket)	
		time.sleep(1)	
		if(komut == "GET"):
			paket = IP( dst = d_ip )/ UDP( sport = 38, dport = 42 )/ Raw( load = dosya_adi)
			send(paket)	#Dosya adı gönderilerek ilgili dosyanın sunucuda olup olmadığı bilgisi beklenir.
				
			dosya_kontrolu = sniff( count = 1, filter = "udp port 38", iface = "lo" )
			test = dosya_kontrolu[0].load.decode()
			if(test == "true"):	#Dosya sunucuda var ise ekleme işlemi gerçekleştirilir.
				get(dosya_adi,d_ip)
				print("İstemciye ekleme işlemi gerçekleştirildi.")
				
			elif(test == "false"):
				print("Server'da " +dosya_adi+ " isminde bir dosya bulunamadı.Tekrar deneyin. ")
	
		
		elif(komut == "PUT"):
			if os.path.exists(dosya_adi) == True:	
				dosya_kontrolu = IP( dst = d_ip )/ UDP( sport = 38, dport = 42 )/ Raw( load = "true")
				send(dosya_kontrolu) #Sunuya yüklenmek istenen dosya istemcide varsa sunucu true ile bilgilendirilir.
				time.sleep(1)		
							
				put(dosya_adi,d_ip)	#Ekleme işlemi gerçekleştirilir.
				print("Sunucuya ekleme işlemi gerçekleştirildi.")
				
			else:
				time.sleep(1)
				dosya_kontrolu = IP( dst = d_ip )/ UDP( sport = 38, dport = 42 )/ Raw( load = "false")
				send(dosya_kontrolu) #Sunuya yüklenmek istenen dosya istemcide yoksa sunucu false ile bilgilendirilir.

				print("İstemcide " +dosya_adi+ " isminde bir dosya bulunamadı.Tekrar deneyin. ")
	elif(komut == '0'):
		print("Program sonlandırıldı.")
		paket = IP( dst = d_ip )/ UDP( sport = 38, dport = 42 )/ Raw( load = '0')
		send(paket)	
		break

	else:
		paket = IP( dst = d_ip )/ UDP( sport = 38, dport = 42 )/ Raw( load = "GECERSIZ")
		send(paket)	
		
		print("Geçersiz komut girişi sağladınız. ")
		print("\nSunucudan dosya getirmek için: GET dosyaAdi ")
		print("Sunucuya dosya yüklemek için: PUT dosyaAdi")
			

	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

