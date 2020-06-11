#!/usr/bin/python3

"""
Ad Soyad:  Onur ETLİĞLU - (180401117)
"""

import socket, os, sys

ip = '127.0.0.1'
port = 42

class Server:
    def __init__(self,addr):
        self.server_address = addr
        self.cwdir = os.getcwd()+"/"
    def connect(self):
        try:
            print(self.server_address,"üzeriden bağlantı kuruluyor...")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print("Socket oluşturuluyor...")
            self.sock.bind(self.server_address)
            print("Sunucu aktiftir:",self.server_address)
        except Exception as e:
            print("Hata oldu:",str(e))
            self.server_close()
    def server_close(self):
        print("Bağlantı kapanıyor...")
        self.sock.close()
        print("Bağlantı kapandı.")
        sys.exit()
    def run(self):
        self.connect()
        print("İstek bekliyor:")
        try: 
            
            while True:
               self.recieved_data, self.client_address = self.sock.recvfrom(4096)
               cmd_seq = self.recieved_data.decode('utf-8').strip().split()
               req = cmd_seq[0].upper()
               print(self.client_address,"'den yeni {} istek geldi".format(req))
               try:
                    handler = getattr(self, req)
                    if req == "PUT" or req == "GET":
                         handler(cmd_seq[1])
                    elif req == "LIST":
                        if len(cmd_seq) > 1:
                            self.sock.sendto(str(req+':'+" yanlış paramatre girdiniz").encode('utf-8'), self.client_address)
                        else:
                            handler()
                         
                    elif req == "QUIT" or req == "EXIT":
                        self.sock.sendto("Oturum sonlandırıldı.".encode('utf-8'), self.client_address)

               except AttributeError as a:
                    if req == "QUIT":
                        self.sock.sendto("Oturum sonlandırıldı.".encode('utf-8'), self.client_address)
                    else:
                        self.sock.sendto("hata yanlış komut".encode('utf-8'), self.client_address)
                        print(str(a))
               except IndexError:
                   self.sock.sendto(str(req+':'+" eksik parametre girdiniz.").encode('utf-8'), self.client_address)
               except Exception as e:
                   self.sock.sendto(str(e).encode('utf-8'),self.client_address)
                   print(str(e))
                   self.server_close()
        except KeyboardInterrupt:
            self.server_close() 
        except Exception as e:
            self.sock.sendto(str(e).encode('utf-8'), self.client_address)
            print(str(e))
    
    
    ## LIST KOMUTU
    def LIST(self):
        data = "PWD: " + self.cwdir + "\n\n"
        paths = os.listdir(self.cwdir)
        for path in paths:
            isDir = os.path.isdir(path)
            if isDir:
                data += "Directory ---> " + self.cwdir + path + "\n"
            else: data +="File --------> " + self.cwdir + path + '\n'
        
        self.sock.sendto(data.encode('utf-8'), self.client_address)


    ## PUT KOMUTU
    def PUT(self, path):
            try:
                self.sock.settimeout(10)
                data, address = self.sock.recvfrom(4096)
                with open(path,'wb') as wfile:
                    while data:
                        wfile.write(data)
                        data, address = self.sock.recvfrom(4096)
                print("Dosya yüklendi")
            except socket.timeout:
                print("Dosya yüklendi")
                self.sock.settimeout(None)
            except Exception as e:
                self.sock.sendto(bytes(str(e),'utf-8'), address)
                print(str(e))
                self.server_close()
   
    ## GET KOMUTU
    def GET(self,path):
        try:
            isfile = os.path.isfile(self.cwdir+path)
            self.sock.sendto(bytes(str(isfile),'utf-8'),self.client_address)
            if not isfile:
                print("Dosya bulunmadı")
            else:
                with open(self.cwdir+path,'rb') as rfile:
                    data = rfile.read(4096)
                    while data:
                        self.sock.sendto(data,self.client_address)
                        data = rfile.read(4096)
        except Exception as e:
            print(str(e))

def main():
    server = Server((ip,port))
    server.run()


main()
