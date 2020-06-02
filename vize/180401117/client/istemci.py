#!/usr/bin/python3

"""
Ad Soyad:  Onur ETLİĞLU - (180401117)
"""

import socket
import sys

class Client:
    def __init__(self, address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (address,port)

    def connect(self):
        print("Bağlantı kuruluyor", self.server_address)
        try:
            print('Bağlandı başaralı oldu:', self.server_address)
            print('\n')
        except KeyboardInterrupt:
            self.close_client()
        except Exception as e:
            print(self.server_address, 'ile bağlantı başarılı olmadı')
            print(e)
            self.close_client()
            
            
    def close_client(self):
        print("Oturum kapanıyor...")
        self.sock.close()
        print("ftp programı çıkıyor...")
        sys.exit(0)
        
    def run(self):
        try:
            self.connect()
        except Exception:
            self.close_client()
        
        self.sock.sendto("LIST".encode('utf-8'),self.server_address)
        cwd = self.sock.recv(4096)
        print(cwd.decode('utf-8'))
        while True:
            try:
                in_cmd = input("Komut Giriniz (list | get | put): ")
                if not in_cmd:
                    continue
                cmd_seq = in_cmd.strip().split()
                req = cmd_seq[0].upper()
                
                self.sock.sendto(in_cmd.strip().encode('utf-8'), self.server_address)
                
                if  req == "QUIT" or req == "EXIT":
                    self.sock.settimeout(10)
                    print(self.sock.recv(4096).decode('utf-8'))
                    self.close_client()
                elif req == "PUT" or req == "GET":
                     if len(cmd_seq)>1:
                         handler = getattr(self, req)
                         handler(cmd_seq[1])
                     else:
                         print(self.sock.recv(4096).decode('utf-8'))
                elif req == "LIST":
                    if len(cmd_seq)>1:
                        print(self.sock.recv(4096).decode('utf-8'))
                    else:
                        handler = getattr(self, req)
                        handler()
                else:
                    print(self.sock.recv(4096).decode('utf-8'))
                print("\n")    
            
            except KeyboardInterrupt:
                self.close_client()
            
            except socket.timeout:
                self.close_client()
                
            except Exception as e:                
                print(str(e))
            
    
    def GET(self,path):
        try:
            self.sock.settimeout(10)
            is_file = bool(self.sock.recv(4096).decode('utf-8'))
            if is_file:
               print("Dosya indriliyor...")
               print("Lütfen bekleyin biraz...")
               data = self.sock.recv(4096)
               with open(path,'wb') as wfile:
                    while data:
                        wfile.write(data)
                        data = self.sock.recv(4096)
                    print("Dosya indirildi.")
            else:
                print("Hata: dosya bulunmadı.")
                
        except socket.timeout:
            print("Dosya indirildi.")
            self.sock.settimeout(None)
            
        except Exception as e:
            print(str(e))
        
    def PUT(self, path):
        try:
            rfile = open(path,'rb')
            file_data = rfile.read(4096)
            print("Dosya yükleniyor...") 
            while file_data:
                self.sock.sendto(file_data, self.server_address)
                file_data = rfile.read(4096)
            self.sock.settimeout(10)
            print("İşlem biraz uzun olabılıyor, bekleyin...")    
            print(self.sock.recv(4096).decode('utf-8'))
        except socket.timeout:
            print("Dosya Yüklendi")
            self.sock.settimeout(None)
        except FileNotFoundError:
            print("Dosya bulunmadı.")
        except Exception as e:
            print(str(e))
    
    def LIST(self):
        print("Dizin listeleniyor...")
        try:  
           dlist = self.sock.recv(4096)
           sys.stdout.write(dlist.decode('utf-8'))
           sys.stdout.flush()
        
        except Exception as e:
            self.sock.close()
            print(str(e))

    
def main():
    address = input("Sunucu Adresi - varsayılan 127.0.0.1: ")
    if not address:
        address = "127.0.0.1"
    port = input("Sunucu Portu - varsayılan 42: ")
    if not port:
       port = 42
        
    client = Client(address, port)
    client.run()
 


main()
    
