#Batuhan Bağçeci - 160401047

import socket
import select
import os
import pickle

def list():
	client.send(b'LIST')

	data = client.recv(1024)
	filelist = pickle.loads(data)

	data = client.recv(1024)
	sizelist = pickle.loads(data)

	fmt = '{:<20}{}'

	print(fmt.format('\033[1m' + 'Dosya', '    Boyut' + '\033[0;0m'))

	for i, (name, size) in enumerate(zip(filelist, sizelist)):
		print(fmt.format(name, str(size) + ' bytes'))

connection = 0

while(True):
	if(connection == 0):
		client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		srvaddr = input('>>>Baglanmak istediginiz sunucu adresi: ')

		client.connect((srvaddr, 42))
		client.send(b'CONNECT')

		client.settimeout(5)
		try:
			data = client.recv(1024)
		except:
			print("[Client]Baglanilamadi! Tekrar deneyin...")
			continue
		client.settimeout(None)

		fmt = '{:<30}{}'

		print('-------------------------------------------------')
		print(fmt.format('\033[1m' + 'GET dosya_ismi' + '\033[0;0m', 'Dosya almayi saglar'))
		print(fmt.format('\033[1m' + 'PUT dosya_yolu' + '\033[0;0m', 'Dosya gondermeyi saglar'))
		print(fmt.format('\033[1m' + 'LIST' + '\033[0;0m', 'Sunucudaki dosyalari listeler'))
		print(fmt.format('\033[1m' + 'DISCONNECT' + '\033[0;0m', 'Oturumu kapatir'))
		print('-------------------------------------------------')

		list()

		connection = 1

	if(connection == 1):
		ready = select.select([client], [client], [])

		data = input('>>>Komut girin: ')

		if(data.upper().startswith('LIST')):
			list()

		elif(data.upper().startswith('GET')):
			client.send(data.encode())

			if ready[0]:
				client.send(data.encode())
			data = data.split()
			name = data[1]

			data = client.recv(1024)

			if(data.decode() == 'Dosya bulunamadi!'):
				print('[Server]' + data.decode())
				continue

			else:
				f = open('./Downloads/' + name, 'wb')

				if ready[1]:
					print('[Client]Indiriliyor...')
					data = client.recv(1024)
					try:
						while(data):
							f.write(data)
							client.settimeout(5)
							data = client.recv(1024)
					except:
						f.close()
						print('[Client]Dosya ./Downloads dizinine indirildi.')
				client.settimeout(None)

		elif(data.upper().startswith('PUT')):
			name = data.split('/')[-1]

			if(os.path.exists(name) and os.path.isfile(name)):
				client.send(data.encode())

				f = open(name, 'rb')
				content = f.read(1024)

				if ready[1]:
					while (content):
						if(client.send(content)):
							print('[Client]Gonderiliyor...')
							content = f.read(1024)
				f.close()
				print('[Client]Gonderildi.')

			else:
				print('[Client]Dosya bulunamadi!')

		elif(data.startswith('DISCONNECT')):
			client.send(data.encode())
			client.close()
			connection = 0
			print('[Client]Oturum kapatildi.')

		else:
			print('[Client]Gecersiz komut girildi!')
