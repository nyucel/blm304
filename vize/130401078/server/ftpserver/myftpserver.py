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


PORT = 42
DPORT = 9999
HOST = "127.0.0.1"

GREEN = '\033[92m'
END = '\033[0m'

class MyFTPServer(ThreadingMixIn, UDPServer):

    def init_setup(self, host=HOST, port=PORT):
         print("Server starting...")
         self.control_channel = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
         print("Binding to address {}:{}...".format(host,port))
         self.control_channel.bind((host,port))
         time.sleep(2)
         print("Initializing env variables...")
         self.cwd = os.getcwd() + "/uploads/"
         self.success = "-Data connection already open; transfer starting"
         self.ac_success = "226-Data connection closed; requested file action was successful."
         self.cli_data = None
         time.sleep(2)
         print("Server is running on address {}:{}".format(host,port))
         print("Active: service "+GREEN+"running"+END+" since %s" % datetime.datetime.now().isoformat(timespec='seconds') )
         print("Waiting for request.")

    def send_response(self,retcode, message):
        print("Sending over control channel {} return code to ".format(retcode) + str(self.client_address))
        self.control_channel.sendto(bytes(str(retcode) + message ,"utf-8"),self.client_address)
        print("Return code successfully sent.")

    def handle_client_request(self,host=HOST, port=PORT):

         self.client_request, self.client_address = self.control_channel.recvfrom(1024)
         cmd_parts = self.client_request.decode().split()
         command = cmd_parts[0]
         print(datetime.datetime.now().isoformat(timespec='seconds') + ': ',end='')
         print("{} request from {}".format(command, self.client_address))

         if len(cmd_parts) == 1:
            if command == "QUIT":
                self.send_response(231,"-User logged out; service terminated.")

            elif command == "LIST":

                dir_contents = self.listdir()
                if type(dir_contents) == tuple:
                    self.send_response(125,self.success)
                elif dir_contents == "EMPTY_DIR":
                    self.send_response(125,self.success)
                else:
                    self.send_response(550,"-Requested action not taken. File unavailable or not found.")

            elif command == "ADAT":
                 self.send_response(220,"-Service ready for new user.")
                 print("New client connected.")


            elif command == "STOR":
                self.send_response(501,"-Syntax error in parameters or arguments.")

            elif command == "RETR":
                self.send_response(501,"-Syntax error in parameters or arguments.")

            else:
                self.send_response(502,"-Command not implemented.")
         else:
            cmd_args = " ".join([ i for i in cmd_parts[1:]]).strip()

            if command == "RETR":

                index = cmd_args.find('/')
                if index != 0:
                    cmd_args = self.cwd + cmd_args

                isFile = os.path.isfile(cmd_args)

                if isFile:
                    self.send_response(125,self.success)
                    self.filename = cmd_args
                else:
                    self.send_response(550,"-Requested action not taken. File unavailable or not found.")


            elif command == "LIST":
                dir_contents = self.listdir(cmd_args)

                if type(dir_contents) == tuple:
                    self.send_response(125,self.success)

                elif dir_contents == "PERMISSION_ERROR":
                    self.send_response(553,"-Requested action not taken. Permission denied.")

                elif dir_contents == "EMPTY_DIR":
                    self.send_response(125,self.success)

                else:
                    self.send_response(550,"-Requested action not taken. File unavailable or not found.")


            elif command == "STOR":
                index = cmd_args.rfind('/')
                if index < 0:
                    cmd_args = self.cwd + cmd_args
                else:
                    cmd_args = self.cwd + cmd_args[index+1:]
                try:
                    self.send_response(125,self.success)
                    self.filename = cmd_args
                except Exception as e:
                        print(e)
                        self.send_response(550,"-Requested action not taken. File unavailable or not found.")



            elif command == "QUIT":
                self.send_response(501,"-Syntax error in parameters or arguments.")

            else:
                self.send_response(502,"-Command not implemented.")



    def listdir(self, path="uploads/"):
        try:
            paths = os.listdir(path)
        except FileNotFoundError:
            return "PATH_ERROR"
        except PermissionError:
            return "PERMISSION_ERROR"
        except Exception:
            return "UNKNOWN_ERROR"

        if len(paths)== 0:
            return "EMPTY_DIR"
        else:
            count = len(max(paths,key=len))

        header = "| %*s | %9s | %10s | %20s | %10s | %10s |"
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
            body += "| %*s | %9s | %10s | %20s | %10s | %10s |\n" % (count, p,filetype,
                    str(stat.st_size) + 'B',time.strftime('%b %d, %Y %H:%M',
                    time.localtime(stat.st_mtime)), oct(stat.st_mode)[-4:], str(stat.st_uid) + '/' + str(stat.st_gid))
        return table,body,footer


class FTPRequestHandler(DatagramRequestHandler):

    def data_channel_open(self):
        print("Starting data transfer...")
        print("Opening data channel...")
        print("Data connection ready for transfer.")
        print("Transfering data...")

    def transfer_data(self, data):
        self.wfile.write(data)


    def data_channel_close(self):
        print("Requested file action okay, completed.")
        print("Closing data channel...")
        print("Data connection closed.")
        print("\nWaiting for new request.")


    def handle(self):
        #cli_data = self.rfile.readline(4096).strip()
        cmd_parts = self.server.client_request.decode().split()
        command = cmd_parts[0]
        print(datetime.datetime.now().__str__() + ': ',end='')
        print("{} request from {}".format(command, self.client_address))

        if len(cmd_parts) == 1:
            if command == "QUIT":
                self.data_channel_open()
                self.transfer_data("231-User logged out; service terminated.".encode('utf-8'))
                self.server.shutdown_request(self.request)
                self.data_channel_close()

            elif command == "LIST":

                dir_contents = self.server.listdir()
                self.data_channel_open()
                if type(dir_contents) == tuple:
                    self.wfile.write(bytes(str("Server PWD: " + self.server.cwd)+"\n","utf-8"))
                    self.transfer_data(bytes(str(dir_contents[0]+dir_contents[1]+dir_contents[2]),"utf-8"))
                    self.wfile.write(bytes(str(self.server.ac_success),"utf-8"))

                elif dir_contents == "EMPTY_DIR":
                    self.tranfer_data(bytes(str("Directory is empty.\n"),"utf-8"))
                    self.wfile.write(bytes(str(self.server.ac_success),"utf-8"))

                else:
                    self.transfer_data("550-Requested action not taken. File unavailable or not found.".encode('utf-8'))
                self.data_channel_close()

            elif command == "ADAT":
                self.data_channel_open()
                self.transfer_data("220-Service ready for new user.".encode('utf-8'))
                self.data_channel_close()

            elif command == "STOR":
                self.data_channel_open()
                self.transfer_data("501-Syntax error in parameters or arguments.".encode('utf-8'))
                self.data_channel_close()

            elif command == "RETR":
                self.data_channel_open()
                self.transfer_data("501-Syntax error in parameters or arguments.".encode('utf-8'))
                self.data_channel_close()
            else:
                self.data_channel_open()
                self.transfer_data("502-Command not implemented.".encode('utf-8'))
                self.data_channel_close()
        else:
            cmd_args = " ".join([ i for i in cmd_parts[1:]]).strip()

            if command == "RETR":
                try:
                    with open(self.server.filename,'rb') as file:
                       self.data_channel_open()
                       fdata = file.readline(4096)
                       while fdata:
                           self.transfer_data(fdata)
                           fdata = file.readline(4096)
                       self.data_channel_close()
                except Exception as e:
                    print(e)
                    self.transfer_data("550-Requested action not taken. File unavailable or not found.".encode('utf-8'))


            elif command == "LIST":
                dir_contents = self.server.listdir(cmd_args)
                self.data_channel_open()
                if type(dir_contents) == tuple:

                    self.wfile.write(bytes(str("Directory: "+cmd_args+"\n"),"utf-8"))
                    self.transfer_data(bytes(str(dir_contents[0]+dir_contents[1]+dir_contents[2]),"utf-8"))
                    self.wfile.write(bytes(str(self.server.ac_success),"utf-8"))

                elif dir_contents == "PERMISSION_ERROR":
                    self.transfer_data("553-Requested action not taken. Permission denied.".encode('utf-8'))

                elif dir_contents == "EMPTY_DIR":
                    self.transfer_data(bytes(str("Directory: "+cmd_args+" is empty\n"),"utf-8"))
                    self.wfile.write(bytes(str(self.server.ac_success),"utf-8"))
                else:
                    self.transfer_data("500-Requested action not taken. File unavailable or not found.".encode('utf-8'))
                self.data_channel_close()

            elif command == "STOR":
                    fdata =  self.rfile.readline(1024).strip()
                    self.data_channel_open()
                    self.server.socket.settimeout(6.5)
                    with open(self.server.filename,'wb') as file:
                        while fdata:
                            file.write(fdata)
                            fdata = self.rfile.readline(1024)
                        self.transfer_data(bytes(str("File has been successfully uploaded  in server uploads directory."),"utf-8"))
                    self.data_channel_close()
            elif command == "QUIT":
                self.data_channel_open()
                self.transfer_data("501-Syntax error in parameters or arguments.".encode('utf-8'))
                self.data_channel_close()

            else:
                self.data_channel_open()
                self.transfer_data("502-Command not implemented.".encode('utf-8'))
                self.data_channel_close()




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
    server = MyFTPServer((HOST,DPORT), FTPRequestHandler)

    pid = os.getpid()

    with open("pid.txt","w") as pfile:
        pfile.write(str(pid)+"\n")

    with server:
        server_thread = threading.Thread(target = server.serve_forever)
        server_thread.daemon = True
        server.init_setup(HOST, PORT)
        server_thread.start()
        while True:
           server.handle_client_request()

        server.shutdown()
        server.socket.close()

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