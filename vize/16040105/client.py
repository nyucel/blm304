import socket
import os

class Client:
    
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect_to_server()

    def connect_to_server():
        hedef_ip = input('Enter ip --> ')
        hedef_port = 42

        s.connect((hedef_ip,hedef_port))

       
    def reconnect():
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect((hedef_ip,hedef_port))


    def main():
        while 1:
            file_name = input('Sunucuya dosya adını girin --> ')
            s.sendto(file_name.encode())

            confirmation = s.recv(1024)
            if confirmation.decode() == "dosya mevcut degil":
                print("Dosya sunucuda mevcut degil")

                s.shutdown(socket.SHUT_RDWR)
                s.close()
                s.reconnect()

            else:        
                write_name = 'from_server '+file_name
                if os.path.exists(write_name): os.remove(write_name)

                with open(write_name,'wb') as file:
                    while 1:
                        data = self.s.recv(1024)

                        if not data:
                            break

                        file.write(data)

                print(file_name,'basariyla indirildi')

		s.shutdown(socket.SHUT_RDWR)
                s.close()
                s.reconnect()
                
client = Client()