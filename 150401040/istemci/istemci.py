#Selin Gül 150401040
#client
import socket
import os
import sys
import time

IP=input("Baglanmak istediginiz sunucunun IP adresini girin: ")
PORT=42
buf=4096
csock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

clientMesaji="Bir istemci baglandi"
iGiden=str.encode(clientMesaji)
try:
	csock.sendto(iGiden,(IP,PORT))#
except:
	print("baglanti hatasi")
	sys.exit()

sGelen=csock.recvfrom(buf)##
liste="Yuklenmis dosyalar  {}".format(sGelen[0].decode('utf-8'))
print(liste)

girdi=input("\n->GET dosyaAdi.dosyaUzantisi\n->PUT dosyaAdi.dosyaUzantisi\n")
komutGiden=str.encode(girdi)
csock.sendto(komutGiden,(IP,PORT))###
komutGiden=girdi.split()
try:
	if (komutGiden[0]=='GET'):
		boyut=csock.recvfrom(buf)[0]
		db=int(boyut.decode())/buf+1
		i=0

		if boyut.decode()=="error":
			print("Yanlis dosya adi girdiniz")
		else:

			f=open("(1)"+komutGiden[1],"wb")
			dosya=csock.recvfrom(buf)[0]
			try:
				while dosya:
					dosya=csock.recvfrom(buf)[0]
					f.write(dosya)
					i+=1
					print("{}. dosya parcasi alindi".format(i))
					csock.settimeout(3)
			except socket.error:
				f.close()
			csock.sendto(b"True",(IP,PORT))	
			csock.close()
			
	elif (komutGiden[0]=='PUT'):
			print("Girilen komut 'PUT' {}\n\n".format(komutGiden[1]))
			dosyaAdi=komutGiden[1]
			dosyalar=os.listdir(os.getcwd())

			if dosyaAdi in dosyalar:
				size=str(os.path.getsize(os.path.abspath(dosyaAdi)))
				msjSize=size.encode()
				f=open(dosyaAdi,"rb")
				dosya=f.read(buf)
				csock.sendto(msjSize,(IP,PORT))
				csock.sendto(dosya,(IP,PORT))

				parcaSayisi=int(size)/buf+1
				i=0
				while dosya:
					if csock.sendto(dosya,(IP,PORT)):
						print("Dosya gonderiliyor...")
						dosya=f.read(buf)
						time.sleep(0.03)
						i+=1
						print("{}. dosya parcasi gonderildi".format(i))
						
				try:
					csock.settimeout(5)
					kontrol=csock.recvfrom(buf)[0].decode()
					print("Dosya Gonderildi")
				
				except socket.timeout:
					f.close()
				csock.close()
				f.close()
			else:
				csock.sendto(b"error",(IP,PORT))
				csock.close()
except socket.error:
	print("BIR HATA BULUNDU")
