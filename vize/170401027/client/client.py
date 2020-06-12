#! usr/bin/env python
# -- coding: UTF-8 --
#python3 client.py 192.168.200.200 list
#python3 client.py 192.168.200.200 get dosya.pdf
#python3 client.py 192.168.200.200 put dosya.pdf
#Egemen Inceler 170401027
from socket import *
import sys
import os
try:
	s = socket(AF_INET, SOCK_DGRAM)
except PermissionError:
	print("Lutfen root olarak calistiriniz.")
host = sys.argv[1]
port = 42
addr = (host,port)
dosyalar="default"

komut = sys.argv[2]
s.sendto(komut.encode("utf-8"), addr)
print("[*]Sunucu ip adresi: ", sys.argv[1], "Port:",port, "\n[*]Komut:", sys.argv[2])
if(port != 42):
	print("Sunucu 42.portu dinliyor.")
	sys.exit()
if(komut.lower() == "list"):
	try:
		dosyalar, clientaddr = s.recvfrom(4096)
		print(dosyalar.decode("utf-8"))
	except :
		print("error")
		sys.exit()
elif(komut.lower() == "put"):
	dosya_adi = sys.argv[3]
	dosya_adi=dosya_adi.encode("utf-8")
	s.sendto(dosya_adi, addr)
	try:
		f= open(dosya_adi, "rb")
		data = f.read(1024)
		while(data):
			if(s.sendto(data, addr)):
				print("gonderiliyor.")
				data = f.read(1024)
		f.close()

		done = "done".encode("utf-8")
		s.sendto(done, addr)
	except FileNotFoundError:
		print("Dosya bulunamadi")
		data = "FileNotFoundError".encode("utf-8")
		s.sendto(data, addr)
		s.close()
	
	
	
elif(komut.lower() == "get"):
	dosya_adi = sys.argv[3]
	dosya_adi = dosya_adi.encode("utf-8")
	s.sendto(dosya_adi, addr)

	f=open(dosya_adi.strip(), 'wb')
	data, addr = s.recvfrom(1024)
	try:
		while(data):
			f.write(data)
			s.settimeout(2)
			data, addr = s.recvfrom(1024)
	except:
		print("Baglanti kesildi.")
	f.close()
	if(data == b"done"):
		print("Dosya basariyla aktarildi.")
	else:
		if(data == b"FileNotFoundError"):
			print("Sunucuda bu dosya bulunamadi.")
			
		print("Dosya aktariminda sorun olustu.")
		os.remove(dosya_adi)
	s.close()
	sys.exit()
