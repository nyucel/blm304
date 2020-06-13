import time
from socket import *

#Furkan Soysal -------------160401017


_Host=str(input("Lütfen Host adresi giriniz..:"))
baglanti=(_Host,142)
client_server=socket(AF_INET,SOCK_STREAM) 

client_server.connect(baglanti)
 

print("client")
# print('{} port {}'.format(*baglanti))
gecikme=client_server.recv(1024).decode()
# print(gecikme.encode())
client_server.sendall(gecikme.encode())

zaman=client_server.recv(1024).decode()

utc=client_server.recv(1024).decode()

client_server.close()
print("\n",zaman)
print("\n",utc)

