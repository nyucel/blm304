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
import os

DEFAULT_PORT = 42
DPORT = 9999
DEFAULT_HOST = "127.0.0.1"


class MyFTPClient(object):

    def __init__(self,server_address):
        self.server_address = server_address
        self.clisocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clisocket.settimeout(5)
        self.downloads = os.getcwd() + "/downloads/"
        try:
            self.clisocket.sendto(bytes("ADAT","utf-8"),self.server_address)
            self.status = str(self.clisocket.recv(1024),"utf-8")
            self.clisocket.setblocking(True)
        except (socket.timeout, OSError):
            print("Connection failed.")
            print("No response from the server.")
            print("Check whether the server is running or not, then retry.")
            sys.exit(0)

    def put(self,command):
         self.clisocket.sendto(bytes(command,"utf-8"),self.server_address)
         data = str(self.clisocket.recv(1024),"utf-8")

         if data[0] == '5': print(data)
         else:
             cmd_parts = command.split()
             if len(cmd_parts) > 1:
                try:
                    filepath = cmd_parts[1].strip()
                    index = filepath.find('/')
                    if index != 0:
                        filepath = self.downloads + filepath
                    isFile = os.path.isfile(filepath)
                    if isFile:
                        print("Uploading file, please wait...")
                        self.dsocket.settimeout(6.5)
                        with open(filepath,'rb') as file:
                            fdata = file.readline(1024)
                            while fdata:
                                self.dsocket.sendto(fdata, (self.server_address[0],DPORT))
                                fdata = file.readline(1024)
                        print(str(self.dsocket.recv(1024),'utf-8'))
                        self.dsocket.recv(1024)
                    else:
                        print("File doesn't exist. Please check the file location and try again.")
                except socket.timeout :
                    self.dsocket.setblocking(True)
                except Exception as e:
                    print("An error occured while uploading file: {}.".format(filepath))
                    print(e)

             else: print(str(self.clisocket.recv(1024),"utf-8"))


    def get(self,command):
         self.clisocket.sendto(bytes(command,"utf-8"), self.server_address)
         data = str(self.clisocket.recv(1024),"utf-8")

         if data[0] == '5': print(data)
         else:
             cmd_parts = command.split()
             if len(cmd_parts) > 1:
                try:
                    filepath = cmd_parts[1].strip()
                    index = filepath.rfind('/')
                    if index < 0:
                        filepath = self.downloads+filepath
                    else: filepath = self.downloads+ filepath[index+1:]

                    with open(filepath,'wb') as file:
                        print("Retrieving file, please wait...")
                        self.dsocket.settimeout(6.5)
                        self.dsocket.sendto(bytes(command,"utf-8"), (self.server_address[0],DPORT))
                        fdata = self.dsocket.recv(1024)
                        while fdata:
                            file.write(fdata)
                            fdata = self.dsocket.recv(1024)
                except socket.timeout :
                    self.dsocket.setblocking(True)
                    print("File has been retrieved successfully, and saved in downloads directory.")
                except Exception as e:
                    print("Retrieving from the server failed.".format(filepath))
                    print(e)

             else: print(str(self.clisocket.recv(1024),"utf-8"))

    def listdir(self,command):
        self.clisocket.sendto(bytes(command,"utf-8"),self.server_address)
        ret_message = str(self.clisocket.recv(2048),"utf-8")
        if ret_message.split('-')[0]=='125':
            print(ret_message)
            self.dsocket.sendto(bytes(command,"utf-8"), (self.server_address[0],DPORT))
            print(str(self.dsocket.recv(25600),"utf-8"))
        else:
            print(ret_message)

    def cwdir(self):
        self.clisocket.sendto(bytes("LIST","utf-8"),self.server_address)
        ret_message = str(self.clisocket.recv(2048),"utf-8")
        if ret_message.split('-')[0]=='125':
            self.dsocket.sendto(bytes("LIST","utf-8"), (self.server_address[0],DPORT))
            data = str(self.dsocket.recv(25600),"utf-8")
            return ret_message + "\n" + data
        else:
            return ret_message

    def disconnect(self,command):
        self.clisocket.sendto(bytes(command,"utf-8"), self.server_address)
        return str(self.clisocket.recv(1024),"utf-8")

    def read_data(self):
        self.dsocket.sendto(bytes("test","utf-8"), (self.server_address[0],DPORT))
        return str(self.dsocket.recv(1024),"utf-8")

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
