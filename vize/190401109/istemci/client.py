#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 21:54:27 2020

@author: Ufuk KORKMAZ
"""

import socket
import os
import sys

class FTPClient:
    def __init__(self, address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.datasock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.data_address = (address,int(port)+1)
        self.server_address = (address,int(port))

    def create_conn(self):
        print("Starting connection to", self.server_address)
        try:
            
            print('Connected to', self.server_address)
            print('\n')
        except KeyboardInterrupt:
            self.close_client()
        except Exception as e:
            print('Connection to', self.server_address, 'failed')
            print(e)
            self.close_client()
            
            
    def close_client(self):
        print("Closing socket connection...")
        self.sock.close()
        print("ftp client exiting...")
        sys.exit(0)
        
    def start(self):
        try:
            self.create_conn()
        except Exception:
            self.close_client()
        print("========== Welcome FTP Program ==========\n")
        self.sock.sendto("LIST".encode('utf-8'),self.server_address)
        cwd = self.sock.recv(1024)
        print(cwd.decode('utf-8'))
        while True:
            try:
                in_cmd = input("|ftp>> ")
                if not in_cmd:
                    continue
                cmd_seq = in_cmd.strip().split()
                req = cmd_seq[0].upper()
                
                self.sock.sendto(in_cmd.strip().encode('utf-8'), self.server_address)
                
                if  req == "QUIT" or req == "EXIT":
                    self.sock.settimeout(6)
                    print(self.sock.recv(1024).decode('utf-8'))
                    self.close_client()
                elif req == "PUT" or req == "GET":
                     if len(cmd_seq)>1:
                         handler = getattr(self, req)
                         handler(cmd_seq[1])
                     else:
                         print(self.sock.recv(1024).decode('utf-8'))
                elif req == "LIST":
                    if len(cmd_seq)>1:
                        print(self.sock.recv(1024).decode('utf-8'))
                    else:
                        handler = getattr(self, req)
                        handler()
                else:
                    print(self.sock.recv(1024).decode('utf-8'))
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
            is_file = bool(self.sock.recv(1024).decode('utf-8'))
            if is_file:
               print("Getting file from server...")
               print("This can take a while...")
               data = self.sock.recv(1024)
               with open(path,'wb') as wfile:
                    while data:
                        wfile.write(data)
                        data = self.sock.recv(1024)
                    print("Retrieving done, but some bytes may have been lost.")
            else:
                print("File Error: file not found or unvailable.")
                
        except socket.timeout:
            print("Retrieving done, but some bytes may have been lost.")
            self.sock.settimeout(None)
            
        except Exception as e:
            print(str(e))
        
    def PUT(self, path):
        try:
            rfile = open(path,'rb')
            file_data = rfile.read(1024)
            print("Storing file to the server...") 
            while file_data:
                self.sock.sendto(file_data, self.server_address)
                file_data = rfile.read(1024)
            self.sock.settimeout(10)
            print("File uploading underway,this can take a while please wait...")    
            print(self.sock.recv(1024).decode('utf-8'))
        except socket.timeout:
            print("Uploading done, but some bytes may have been lost.")
            self.sock.settimeout(None)
        except FileNotFoundError:
            print("File does not exist or unvailable.")
        except Exception as e:
            print(str(e))
    
    def LIST(self):
        print("Listing current directory...")
        try:  
           dlist = self.sock.recv(1024)
           sys.stdout.write(dlist.decode('utf-8'))
           sys.stdout.flush()
        
        except Exception as e:
            self.sock.close()
            print(str(e))



class Client(object):
    
    def run_forever(self):
        addr = input("Server IP (default = 127.0.0.1): ")
        if not addr:
            addr = "127.0.0.1"
        port = input("Server Port (default = 42): ")
        if not port:
            port = 42
        
        self.ftp_client = FTPClient(addr, port)
        self.ftp_client.start()
 
if __name__ == "__main__":
    Client().run_forever()
    
