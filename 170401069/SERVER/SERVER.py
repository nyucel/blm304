
#Ramazan ŞAHİN  170401069

#SERVER

import socket,os
import platform

if __name__ == "__main__":
    ########### Isletim Sistemi Kontrolu ###########
    os_inf = platform.system()
    if os_inf == "Linux":
        os.system("clear")
    elif os_inf == "Windows":
        os.system("cls")
    print('SERVER')

HOST=""
PORT=42
SİZE=1024
main_server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
main_server.bind((HOST,PORT))
client_command,address = main_server.recvfrom(SİZE)
client_command = client_command.decode('utf-8').strip()
print(client_command)

def a():
	path = os.getcwd()
	return str(os.listdir(path))
main_server.sendto(a().encode('utf-8'),address)

a,b = main_server.recvfrom(SİZE)
a=a.decode('utf-8').strip()

if a=="get" or a == "GET":
	dosya_ismi,adres=main_server.recvfrom(SİZE)     # dosya ismini aldık
	dosya_ismi = dosya_ismi.decode('utf-8').strip() 
	
	new_file=open(dosya_ismi,"rb")
	i = new_file.read(SİZE)
	while i:
		main_server.sendto(i,address)
		i = new_file.read(SİZE)
	print("[+][+] Dosya Başarılı Bir Şekilde Aktarıldı [+][+]")	
	new_file.close()
	
if a == "put" or a == "PUT":
	dosya_ismi,adres=main_server.recvfrom(SİZE)
	dosya_ismi = dosya_ismi.decode('utf-8').strip()
	x,address = main_server.recvfrom(SİZE)
	f = open(dosya_ismi,"wb")
	try:
		while x:
			f.write(x)
			main_server.settimeout(3)
			x,address = main_server.recvfrom(SİZE)
			
	except socket.timeout:
		f.close()
		print("[+][+] Dosya Başarılı Bir Şekilde Aktarıldı [+][+]")
	







