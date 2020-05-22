#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date Mon May 18 09:57:49 2020

@author Abdoul Karim TOURE
@contact contact@trabdlkarim.com
@copyright Copyright 2020, Abdoul Karim TOURE
@license GPL v3.0 or Later
@version 1.0.1
@status Development
"""

import sys
import os
import cmd
import time 

from ftpclient import myftpclient as client
from scapy.all import *

class MyFTPShell(cmd.Cmd):
    intro ="Welcome to MyFTP Shell.\n"
    intro += "Type 'help' or '?' to list all available commands.\n\n"
    intro += "Author: Abdoul Karim TOURE\n"
    intro += "MyFTP 1.0.1 -- A Simple FTP Client using UDP\n\n"
    prompt="myftp> "
    
    def preloop(self):
        print("Connecting to the server...")
        time.sleep(2)
        print("Host: {}".format(self.cmd_args['remote']))
        print("Port: {}".format(self.cmd_args['port']))
        time.sleep(3)
        self.myftpclient = client.MyFTPClient((self.cmd_args['remote'],self.cmd_args['port']))
        print("Successfully connected.\n")
        
    # ----- basic ftp shell commands -----
    def do_put(self, arg):
        self.myftpclient.put("STOR " + arg)
    
    def help_put(self):
        print("Store a local file on the remote machine.")
    
    def do_get(self, arg):
        self.myftpclient.get("RETR " + arg)
        
    def help_get(self):
        print("Retrieve a file from the remote and store it on the local machine.")
    
    def do_list(self,arg):
        self.myftpclient.listdir("LIST " + arg)
    
    def help_list(self):
        print("Print a listing of the contents of a directory on the remote machine.")
        
    def do_bye(self,arg):
        self.myftpclient.disconnect("QUIT " + arg)
        return True
    
    def help_bye(self):
        print("Terminate the FTP session with the remote server, and return to the command interpreter.")
        
    
    def do_quit(self,arg):
        self.myftpclient.disconnect("QUIT " + arg)
        return True

    def help_quit(self):
        print("A synomym for bye.")
    

    def do_exit(self,arg):
        self.myftpclient.disconnect("QUIT " + arg)
        return True
    
    def help_exit(self):
        print("A synonym for bye.")
    
    def parse_args(self,argv):
        self.cmd_args = client.parse_args(argv)
        
    def postloop(self):
        print("Thank you for using myftp.")
        print("Bye, see you soon!")        
    



def listdir(path ='.'):
    for file in os.listdir(path):
        print(os.path.join(path, file))


def main(argv):
    shell = MyFTPShell()
    shell.parse_args(argv)
    shell.cmdloop()
    



if __name__ == "__main__":
   print("You shouldn't be running this module, rather run myftp.py.")
    