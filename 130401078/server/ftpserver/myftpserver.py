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
import datetime
import argparse as arg
from socketserver import UDPServer
from socketserver import ThreadingMixIn 
from socketserver import DatagramRequestHandler


PORT = 9998
DPORT = 9999
HOST = "127.0.0.1"

class MyFTPServer(ThreadingMixIn, UDPServer):
    
    def start_message(self,host, port):
        print("Starting server...")
        time.sleep(2)
        print("Host: %s" % host)
        print("Port: %i" % port)
    
    
class FTPRequestHandler(DatagramRequestHandler):
    
    def handle(self):
        # cli_req = self.request[0].strip()
        #socket = self.request[1]
        cli_req = self.rfile.readline().strip()
        cmd_parts = cli_req.split()
        command = str(cmd_parts[0],"utf-8")
        if command=="QUIT":
            self.server.shutdown_request(self.request)
            print(datetime.datetime.now().__str__() + ': ',end='')
            print("{} request from {}".format(command, self.client_address))
            print("{} terminated session.".format(self.client_address))
            
        else:
            cur_thread = threading.current_thread()
            print("Current thread:",cur_thread.name)
            print(datetime.datetime.now().__str__() + ': ',end='')
            print("{} request from {}".format(command, self.client_address))  
            #socket.sendto(bytes(command + " Request","utf-8"),self.client_address)
            self.wfile.write(bytes(command + " Request","utf-8"))    



def parse_args(argv):
    parser = arg.ArgumentParser(prog="myftserver",description="description: simple FTP server using UDP protocol")
    group = parser.add_mutually_exclusive_group()
    global PORT
    parser.add_argument("-p","--port",type=int, default=PORT,
                        help="define the server's listening port")
    group.add_argument("--start", action='store_true', help="start the ftp server")
    group.add_argument("--stop",action="store_true", help="stop the ftp server  ")
    
    parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0.1')
    args =  parser.parse_args(argv)
    args = vars(args) 
    PORT = args['port']

    return parser, args


def start_server():
    server = MyFTPServer((HOST,PORT), FTPRequestHandler)
    pid = os.getpid()
    with open("pid.txt","w") as pfile:
        pfile.write(str(pid)+"\n")
        
    with server:
        server_thread = threading.Thread(target = server.serve_forever)
        server_thread.name =" myftpserver_main_thread"
        server_thread.daemon = True
        server.start_message(HOST,PORT)
        server_thread.start()
       
        
        print("Server is running.")
        print("Waiting for resquest.")
        while True:
            pass
        server.shutdown()


def stop_server():
    with open("pid.txt",'r') as pfile:
        pid = pfile.readline()
        pid = int(str(pid).strip())
    
    try:
        os.kill(pid,2)
        print("Server has been stopped.")
    except ProcessLookupError:
        print("Server has already stopped.")



def main(argv):
    parser, args = parse_args(argv)
    if args["start"] == True:
        try:
            start_server()
        except (KeyboardInterrupt,SystemExit):
            print("\nServer stopped.")
            
    elif args["stop"] ==True:
        stop_server()
        
    else:
        parser.print_help()


if __name__=="__main__":
    main(sys.argv[1:])