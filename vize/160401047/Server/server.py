#Batuhan Bağçeci - 160401047

import socket
import select
import os
import pickle

address = '0.0.0.0'

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((address, 42))

print('[Server]Sunucu baslatildi...')

while(True):
	ready = select.select([server], [server], [])

	data, cliaddr = server.recvfrom(1024)
	data = data.decode()
	print('[Client]' + data)

	if(data.upper().startswith('CONNECT')):
		server.sendto(b'1', cliaddr)

	if(data.upper().startswith('LIST')):
		filelist = os.listdir('./FTP')
		sizelist = []

		for filename in filelist:
			sizelist.append(os.path.getsize('./FTP/' + filename))
			
		data = pickle.dumps(filelist)
		server.sendto(data, cliaddr)

		data = pickle.dumps(sizelist)
		server.sendto(data, cliaddr)

	elif(data.upper().startswith('GET')):
		data = data.split()

		if(data[1] in  os.listdir('./FTP')):
			if ready[1]:
				server.sendto(b'1', cliaddr)

			f = open('./FTP/'+data[1], 'rb')
			content = f.read(1024)

			if ready[1]:
				while(content):
					if(server.sendto(content, cliaddr)):
						print('[Server]Gonderiliyor...')
						content = f.read(1024)
			f.close()
			print('[Server]Gonderildi.')

		else:
			if ready[1]:
				server.sendto(b'Dosya bulunamadi!', cliaddr)
				print('[Server]Dosya bulunamadi!')

	elif(data.upper().startswith('PUT')):
		name = data.split('/')[-1]

		f = open('./FTP/'+name, 'wb')

		if ready[1]:
			print('[Server]Indiriliyor...')
			data = server.recv(1024)
			try:
				while(data):
					f.write(data)
					server.settimeout(5)
					data = server.recv(1024)
			except:
				f.close()
				print('[Server]Dosya indirildi.')
		server.settimeout(None)

	else:
		continue
