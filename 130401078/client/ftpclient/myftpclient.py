#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date Sat May 16 12:08:50 2020

@author Abdoul Karim TOURE
@contact contact@trabdlkarim.com
@copyright Copyright 2020, Abdoul Karim TOURE
@license GPL v3.0 or Later
@version 1.0.1
@status Development

"""
import socket
import time
import argparse as arg
import sys


DEFAULT_PORT = 9998
DATA_PORT = 9999
DEFAULT_HOST = "127.0.0.1"


class MyFTPClient(object):
    
    def __init__(self,server_address):
        self.server_address = server_address
        self.clisocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clisocket.settimeout(5)
       
        try:
            self.clisocket.sendto(bytes("ADAT","utf-8"),self.server_address)
            self.status = str(self.clisocket.recv(1024),"utf-8")
        except (socket.timeout, OSError):
            print("Connection failed.")
            print("No response from the server.")
            print("Check whether the server is running or not, then retry.")
            sys.exit(0)
        
    def put(self,command):
        self.clisocket.sendto(bytes(command,"utf-8"),self.server_address)
        print(str(self.clisocket.recv(1024),"utf-8"))
        
        
    def get(self,command):
        self.clisocket.sendto(bytes(command,"utf-8"), self.server_address)
        print(str(self.clisocket.recv(1024),"utf-8"))
        

    def listdir(self,command):
        self.clisocket.sendto(bytes(command,"utf-8"),self.server_address)
        print(str(self.clisocket.recv(25600),"utf-8"))
        
        
    def disconnect(self,command):
        self.clisocket.sendto(bytes(command,"utf-8"),self.server_address)
        print(str(self.clisocket.recv(1024),"utf-8"))
        

def parse_args(argv):
    
    parser = arg.ArgumentParser(prog="myftp",description="description: Simple FTP Client using UDP")
    parser.add_argument("-p","--port",type=int, default=DEFAULT_PORT,
                        help="server listening port")
    parser.add_argument("-r","--remote", default=DEFAULT_HOST, help="remote host IP address ")
    parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0.1')
    args =  parser.parse_args(argv)
    args = vars(args)
    
    return args
 


if __name__=="__main__":
    print("You shouldn't be running this module, rather run myftp.py.")
    