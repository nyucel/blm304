#Batuhan Bagceci - 160401047

import socket
import datetime
import subprocess
import shlex

PORT = 142

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while(True):
	ADDRESS = input("Baglanmak istediginiz adres: ")

	client.settimeout(5)
	try:
		client.connect((ADDRESS, PORT))
		break
	except:
		print("Baglanilamadi!!! Tekrar Deneyin...")
		continue

client.settimeout(None)

while(True):
	usr_inp = input("Saati ayarlamak için [ENTER] cikmak icin [HERHANGİ BİR TUS+ENTER]: ")

	if(usr_inp == ""):
		delay_start = datetime.datetime.utcnow().timestamp()
		client.send("1".encode())
		TIME, TIMEZONE = client.recv(1024).decode().split("@")
		delay_end = datetime.datetime.utcnow().timestamp()

		delay = ((delay_end - delay_start) / 2) * 1000
		TIME = float(TIME) + delay
		TIME = datetime.datetime.fromtimestamp(float(TIME) / 1000)

		print("Sunucu zamani:", (TIME.strftime("%b %d %Y %H:%M:%S.%f")[:-3]), TIMEZONE)

		try:
			subprocess.call(shlex.split("sudo date -s '%s'" %TIME))
			print("Saat ve tarih ayarlandi.")
		except:
			print("Saat ve tarih ayarlanirken hata olustu...")

	else:
		client.send("0".encode())
		client.close()
		break
