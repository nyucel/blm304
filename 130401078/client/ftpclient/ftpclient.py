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
import sys
import argparse as arg

DEFAULT_PORT = 9999
DEFAULT_HOST = "127.0.0.1"


class FTPClient(object):
    
    def __init__(self,sock,data):
        self.sock = sock
        self.data = data
        self.clisocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        
    def PUT(self):
        self.clisocket.sendto(bytes(self.data+"\n","utf-8"),self.sock)
        
        
        
    def GET(self):
        self.received = str(self.clisocket.recv(1024),"utf-8")
        print("Sent: {}".format(self.data))
        print("Received: {}".format(self.received))
        

    def LIST(self):
        pass

def main(argv):
    
    parser = arg.ArgumentParser(description="FTP Client using UDP")
    parser.add_argument("-p","--port",type=int, default=DEFAULT_PORT,
                        help="server listening port")
    parser.add_argument("-r","--remote", default=DEFAULT_HOST, help="remote host IP address ")
    parser.add_argument("-m","--message", default="Hello World", help="message to be sent to remote ")
    parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0.1')
    args =  parser.parse_args(argv)
    args = vars(args)
    print(args)
    ftpcli = FTPClient((args['remote'],args['port']),args['message'])
    ftpcli.put()
    ftpcli.get()
        


if __name__=="__main__":
    #main(sys.argv[1:]) 
    print("All good.")