import socket
import os

class Server:
    
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.accept_connections()
    
    def accept_connections():
        ip = socket.gethostbyname(socket.gethostname())
        port = 42
        s.bind((ip,port))
        s.listen(5)

        print('IP: '+ip)
        print(' port: '+port)

        while 1:
            c, addr = s.accept()
            print(c)
            
     def List()
	msg = "Komut doğru "
	msgEn = msg.encode('utf-8')
	socket.sendto(msgEn,clientAddr)
	F =os.listdir(path=...............)

	Lists =[]
	for file in F
		Lists.append(file)
	ListsStr = str(Lists)
	ListsEn = Lists.encode('utf-8')
	socket.sendto(Lists, clientAddr)
	print("Liste gönderiliyor")

     def Exit():
    	print(" soketim kapatiliyor...")
	s.close()
	sys.exit()
       

    def GET():
        data = c.recv(1024).decode()
    
        if not os.path.exists(data):
            c.send("dosya mevcut degil".encode())

        else:
            c.send("dosya mevcut".encode())
            print('Gonderiliyor...',data)
            if data != '':
                file = open(data,'rb')
                data = file.read(1024)
                while data:
                    c.send(data)
                    data = file.read(1024)

                c.shutdown(socket.SHUT_RDWR)
                c.close()
                

server = Server()

