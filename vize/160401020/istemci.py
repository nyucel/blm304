import socket
import os
import tempfile

#MUCAHİD TAM 160401020

# Ftp den GEt ile istenen dosya /tmp altina indirilir

localIp=str(input("FTP adresini giriniz : "))
serverAddressPort = (localIp,42)

UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
	print ("\nUsage : LIST or GET/PUT <fullpath>")
	input_string = input("Command: ")

	input_s = input_string.split()

	if len(input_s) == 0:
		continue

	if input_s[0] == "LIST":
		UDPClientSocket.sendto(input_s[0].encode(), serverAddressPort)
		msgFromServer, address = UDPClientSocket.recvfrom(1024)
		msgFromServer = eval(msgFromServer.decode())
		if len(msgFromServer) > 0:
			for f in msgFromServer:
				print(f)
		else:
			print("There is no file...")
	elif input_s[0] == "GET" and len(input_s) == 2:
		UDPClientSocket.sendto(",".join(input_s).encode(), serverAddressPort)

		msglis, address = UDPClientSocket.recvfrom(1024) 
		filename = msglis.decode().split(',')[1]
		f = open(tempfile.gettempdir()+"/"+filename,'wb')      #open that file or create one
		l, address = UDPClientSocket.recvfrom(1024)         #get input
		print ("Receiving...File Data")
		try:
			while (l):
				try:
				    if len(l) < 15 and l.decode() == "!!FINISHED!!":       #get again until done
				        break;
				except:
					continue
				f.write(l)      #save input to file
				l, address = UDPClientSocket.recvfrom(1024)

			print ("Received...File Data")
			f.close()
		except:
			print ("Receiving file is failed!!!")
	elif input_s[0] == "PUT" and len(input_s) == 2:
		if os.path.isfile(input_s[1]):
			path = input_s[1] 
		else:
		    print ("File not exist")
		    exit(0)

		print ("sending file")

		filename=os.path.basename(path)
		UDPClientSocket.sendto(("PUT," + filename).encode('utf-8'), serverAddressPort)

		with open(path,'rb') as f:
			l = f.read(1024)
			while (l):
				UDPClientSocket.sendto(l, serverAddressPort)
				l = f.read(1024)
			UDPClientSocket.sendto("!!FINISHED!!".encode(), serverAddressPort)

		print ("file sent")

	else:
		print ("Unkown Command! Usage : LIST or GET/PUT <fullpath>")