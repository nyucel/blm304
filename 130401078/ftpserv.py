#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date Sat May 16 12:05:20 2020

@author Abdoul Karim TOURE
@contact contact@trabdlkarim.com
@copyright Copyright 2020, Abdoul Karim TOURE
@license GPL v3.0 or Later
@version 1.0.1
@status Development

"""
import os
import sys
import threading
import time
import argparse as arg
from socketserver import UDPServer 
from socketserver import BaseRequestHandler

DEFAULT_PORT = 9999
DEFAULT_HOST = "127.0.0.1"

class FTPServer(UDPServer):
    def __init__(self,socket, handler):
        super().__init__(socket, handler)
    
    def start(self):
        print("Server starting...")
        super().serve_forever()
        print("Server is running.")
        print("Host: {}"%DEFAULT_HOST)
        print("Port: {}"%DEFAULT_PORT)
        
    def stop(self):
        print("Server stopping...")
        super().server_close()
        print("Server stopped")
    
class FTPRequestHandler(BaseRequestHandler):
    
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        socket.sendto(data.upper(),self.client_address)
        


def main(argv):
    parser = arg.ArgumentParser(description="FTP Server using UDP")
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("-p","--port",type=int, default=DEFAULT_PORT,
                        help="server listening port")
    group.add_argument("--start", action='store_true', help="start remote")
    group.add_argument("--stop",action="store_true", help="stop remote ")
    
    parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0.1')
    args =  parser.parse_args(argv)
    args = vars(args)
    print(args)
    
    
    with FTPServer((DEFAULT_HOST,DEFAULT_PORT), FTPRequestHandler) as server:
        if args["start"] == True:
            server.start()
        else:
            server.stop()













if __name__=="__main__":
    main(sys.argv[1:])