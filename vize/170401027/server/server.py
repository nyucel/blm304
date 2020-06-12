#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#python3 server.py
#Egemen Inceler 170401027
from socket import *
import sys
import select
import os

host ="192.168.0.28"  #server adress
port = 42

s = socket(AF_INET, SOCK_DGRAM)
try:
	s.bind((host, port))
except PermissionError:
	print("Lutfen root olarak calistiriniz.")
	sys.exit()
addr = ((host, port))
done= " "
def serverListele():
	F = (os.listdir())
	
	lists_str = str(F)
	listsEn = lists_str.encode("utf-8")
	s.sendto(listsEn, addr)
	print(listsEn.decode("utf-8"), addr)
	print("Konumdaki dosyalar listelendi.")


def dosyacek():
	data, addr = s.recvfrom(1024)
	data = data.decode("utf-8")
	print("Indirilecek dosya:",data.strip())
	dosya = data.strip()
	f=open(data.strip(), 'wb')
	data, addr = s.recvfrom(1024)
	try:
		while(data):
			f.write(data)
			s.settimeout(2)
			data, addr = s.recvfrom(1024)
	except Exception as e:
		f.close()
		#print(e)

	f.close()
	
	if(data == b"done"):
		print("Dosya basariyla aktarildi")
	elif(data == b"FileNotFoundError"):
		print("Dosya bulunamadi.")
		os.remove(dosya)
	else:
		print("Dosya aktariminda sorun olustu.")
		os.remove(dosya)
def dosyaGonder():
	data, addr = s.recvfrom(1024)
	data = data.decode("utf-8")
	print("karsiya yollanacak dosya: ", data.strip())
	dosya_adi = data.strip()
	try:
		f= open(dosya_adi, "rb")
		data = f.read(1024)
		while(data):
			if(s.sendto(data, addr)):
				print("gonderiliyor")
				data = f.read(1024)
		f.close()
		done = "done".encode("utf-8")
		s.sendto(done, addr)
		
		
	except FileNotFoundError:
		print("Dosya bulunamadi")
		data = "FileNotFoundError".encode("utf-8")
		s.sendto(data, addr)
		s.close()
while(True):
	print("dinleniyor")
	data, addr = s.recvfrom(1024)
	text = data.decode("utf-8")
	komut=(text.split())


	if(komut[0].lower() == "list"):
		print("listeleniyor")
		serverListele()
		s.close()
		break
		sys.exit()

	if(komut[0].lower() == "put"):
		print("Dosya cekiliyor.")
		dosyacek()
		s.close()
		break
		sys.exit()
				
		
	if(komut[0].lower() == "get"):
		print("Dosya gonderiliyor.")
		dosyaGonder()
		s.close()
		break
		sys.exit()
