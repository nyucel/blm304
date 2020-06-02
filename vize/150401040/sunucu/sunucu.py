
#Selin Gül -150401040
#server
import socket
import os
import time
import sys

IP='127.0.0.1'
PORT=42
buf=4096
print("IP adresi:{}, PORT: 42\n".format(IP))

while 1:
	try:
		ssock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		ssock.bind((IP,PORT))
		print("{}. port dinleniyor".format(PORT))
		ibaglanti, cAdres=ssock.recvfrom(buf)#
		itext=ibaglanti.decode('utf-8')
		print(itext)
		
		#bulundugumuz dizindeki dosyalari listeliyoruz
		Dizin=os.listdir(os.getcwd())
		Liste=[]
		for dosya in Dizin:
			Liste.append(dosya)
		mesaj=str(Liste)
		enMesaj=str.encode(mesaj)
		ssock.sendto(enMesaj,cAdres)##

		baglanti,cAdres=ssock.recvfrom(buf)###
		text=baglanti.decode('utf-8')
		komut=text.split()
		if(komut[0]=='GET'):
			print("Girilen komut 'GET' {}\n\n".format(komut[1]))
			dosyaAdi=komut[1]
			dosyalar=os.listdir(os.getcwd())

			if dosyaAdi in dosyalar:
				size=str(os.path.getsize(os.path.abspath(dosyaAdi))) #dosya buyuklugu
				msjSize=size.encode()
				f=open(dosyaAdi,"rb")
				dosya=f.read(buf)
				ssock.sendto(msjSize,cAdres)
				ssock.sendto(dosya,cAdres)

				parcaSayisi=int(size)/buf+1
				i=0
				while dosya:
					if ssock.sendto(dosya,cAdres):
						print("{}. dosya parcasi gonderildi".format(i))
						dosya=f.read(buf)
						time.sleep(0.03)
						i+=1
						
				try:
					ssock.settimeout(3)
					kontrol=ssock.recvfrom(buf)[0].decode()
					if(kontrol=='True'):
						print("Dosya Gonderildi")
				
				except socket.error:
					print("Dosya Gonderilemedi")
				#if(i<int(size)):
					#print("gonderilemedi")
				ssock.close()
				f.close()
			else:
				ssock.sendto(b"error",cAdres)
				ssock.close()

		elif(komut[0]=='PUT'):
			print("Girilen komut 'PUT' {}".format(komut[1]))
			boyut=ssock.recvfrom(buf)[0]

			if boyut.decode()=="error":
				print("Yanlis dosya adi girildi")
			else:
				db=int(boyut.decode())/buf+1
				print(boyut.decode())
				i=0
				f=open(komut[1],"wb")
				dosya=ssock.recvfrom(buf)[0]
				try:
					while dosya:
						dosya=ssock.recvfrom(buf)[0]
						f.write(dosya)
						i+=1
						print(i)
						ssock.settimeout(3)
				except socket.timeout:
					f.close()
				ssock.sendto(b"True",cAdres)	
				ssock.close()

		else:
			print("Yanlıs komut girdiniz")		
	except socket.timeout:
		print("HATAAAAAAAAA")	