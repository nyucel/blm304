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
import socket
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
    
    def start_message(self, host, port):
        print("Starting server...")
        time.sleep(2)
        print("Host: %s" % host)
        print("Port: %i" % port)
    
    def open_data_socket(self):
        print("Opening data connection for transfer...")
        time.sleep(1)
        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.data_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.data_socket.bind((HOST,DPORT))
        print("Data connection ready for transfer.")


    def close_data_socket(self):
       print("Requested file action was successful. ")
       print("Closing data connection...")
       time.sleep(1)
       self.data_socket.close()
       print("Data connection closed.")
    
    def waiting_message(self):
        print("\nWaiting for new request.")
    
    def listdir(self, path="uploads/"):
        self.cwd = os.getcwd() + "/uploads"
        try:
            paths = os.listdir(path)
        except FileNotFoundError:
            return "PATH_ERROR"
        
        if len(paths)== 0:
            count = 0
            return None
        else:
            count = len(max(paths,key=len))
            
        header = "| %*s | %9s | %12s | %20s | %11s | %12s |" 
        header = header % (count,"Name","Filetype","Filesize","Last Modified","Permission","User/Group")
        table = '%s\n%s\n%s\n' % ('-' * len(header), header, '-' * len(header))
        footer = '%s\n' % ('-' * len(header))
        body = ""
        for p in paths:
            fpath = os.path.join(path,p)
            stat = os.stat(path)
            filetype = None
            if os.path.isdir(fpath):
                filetype= "Directory"
            else:
                filetype = "File"
            body += "| %*s | %9s | %12s | %20s | %11s | %12s |\n" % (count, p,filetype, 
                    str(stat.st_size) + 'B',time.strftime('%b %d, %Y %H:%M',
                    time.localtime(stat.st_mtime)), oct(stat.st_mode)[-4:], str(stat.st_uid) + '/' + str(stat.st_gid))
        return table,body,footer

                                               
class FTPRequestHandler(DatagramRequestHandler):
    def send_response(self,retcode, message):
        print("Sending response to " + str(self.client_address) +'.')
        self.wfile.write(bytes(str(retcode) + message ,"utf-8"))
        print("Response sent.")
        
    def transfert_data(self,data):
        print("Starting data transfer...")
        self.server.open_data_socket()
        print("Transfering data to {}".format(self.client_address))
        self.wfile.write(bytes(str(data) ,"utf-8"))
        self.server.close_data_socket()
        
    def handle(self):
        # cli_req = self.request[0].strip()
        #socket = self.request[1]
        cli_req = self.rfile.readline().strip()
        cmd_parts = cli_req.decode().split()
        command = cmd_parts[0]
        
        print(datetime.datetime.now().__str__() + ': ',end='')
        print("{} request from {}".format(command, self.client_address))
        
        if len(cmd_parts) == 1:
            if command == "QUIT":
                self.send_response(231,"-User logged out; service terminated.")
                self.server.shutdown_request(self.request)
            
            elif command == "LIST":
                self.send_response(125,"-Data connection already open; transfer starting.\n")
                dir_contents = self.server.listdir()
                self.wfile.write(bytes(str("Current Directory: " + self.server.cwd+"\n"),"utf-8"))
                if dir_contents:
                    
                    self.wfile.write(bytes(str(dir_contents[0]),"utf-8"))
                    self.transfert_data(dir_contents[1])
                    self.wfile.write(bytes(str(dir_contents[2]),"utf-8"))
                    
                else:
                    self.wfile.write(bytes(str("Directory Empty\n"),"utf-8"))
                    
                self.send_response(226,"-Closing data connection. Requested file action  was successful.")
                self.server.waiting_message()
                
            elif command == "ADAT":
                 self.send_response(220,"-Service ready for new user.")
                 print("New client connected.")
                 self.server.waiting_message()
            else:
               self.send_response(501,"-Syntax error in parameters or arguments")
               self.server.waiting_message()
        else:
            cmd_args = " ".join([ i for i in cmd_parts[1:]]).strip()
            if command == "RETR":
                self.send_response(125,"-Data connection already open; transfer starting.")
                self.send_response(226,"-Closing data connection. Requested file action was successful.")
                self.server.waiting_message()
                
            elif command == "LIST":
                dir_contents = self.server.listdir(cmd_args)
                
                if (dir_contents != None) and (dir_contents != "PATH_ERROR"):
                    self.wfile.write(bytes(str("Current Directory: " + self.server.cwd+"\n"),"utf-8"))
                    self.send_response(125,"-Data connection already open; transfer starting.\n")
                    self.wfile.write(bytes(str(dir_contents[0]),"utf-8"))
                    self.transfert_data(dir_contents[1])
                    self.wfile.write(bytes(str(dir_contents[2]),"utf-8"))
                    self.send_response(226,"-Closing data connection. Requested file action successful")
                    
                    
                elif dir_contents == "PATH_ERROR":
                    self.send_response(550,"-Requested action not taken. File unavailable or not found.")
                elif dir_contents == None:
                    self.wfile.write(bytes(str("Current Directory: " + self.server.cwd+"\n"),"utf-8"))
                    self.wfile.write(bytes(str("Directory Empty\n"),"utf-8"))
                    
               
                self.server.waiting_message()
                
            elif command == "STOR":
                self.send_response(125,"-Data connection already open; transfer starting.\n")
                self.send_response(226,"-Closing data connection. Requested file action successful")
                self.server.waiting_message()
            else:
                self.send_response(502,"-Command not implemented.")
                self.server.waiting_message()


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
        global count 
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
        print("Can't stop server, because it not running.")



def main(argv):
    parser, args = parse_args(argv)
    if args["start"] == True:
        try:
            start_server()
        except (KeyboardInterrupt,SystemExit):
            print("\nServer stopped.")
            
    elif args["stop"] == True:
        stop_server()
        
    else:
        parser.print_help()


if __name__=="__main__":
    print("You shouldn't be running this module, rather run server.py")