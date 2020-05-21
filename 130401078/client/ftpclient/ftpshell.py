#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:57:49 2020

@author: trabdlkarim
"""

import sys
import os
import cmd

import ftpclient as client

class FTPShell(cmd.Cmd):
    intro ="Welcome to MyFTP Shell.\n"
    intro += "This is a FTP client using UDP protocol.\n"
    intro += "Type 'help' or '?' to list all available commands.\n\n"
    intro += "Author: Abdoul Karim TOURE\n"
    intro += "MyFTP 1.0.1 -- A Simple Custom FTP Client\n"
    prompt="myftp> "
    file = None
    
    # ----- basic ftp shell commands -----
    def do_put(self, arg):
        self.data = arg.upper()
        print("saving data...")
        print("%s has been saved" % arg)
    
    def help_put(self):
        print("Store a local file on the remote machine.")
    
    def do_get(self, arg):
        print("getting data...")
        print("received: %s" % self.data)
        
    def help_get(self):
        print("Retrieve a file from the remote and store it on the local machine.")
    
    def do_list(self,arg):
        if len(arg) == 0:
            listdir()
        else: listdir(arg)
    
    def help_list(self):
        print("Print a listing of the contents of a directory on the remote machine.")
        
    def do_bye(self,arg):
        display_message()
        return True
    
    def help_bye(self):
        print("Terminate the FTP session with the remote server, and return to the command interpreter.")
        
    
    def do_quit(self,arg):
        display_message()
        return True

    def help_quit(self):
        print("A synomym for bye.")
    

    def do_exit(self,arg):
        display_message()
        return True
    
    def help_exit(self):
        print("A synonym for bye.")
    
    


def display_message():
    print("FTP session terminated.")
    print("Thank you for using MyFTP.")
    print("Bye, see you soon!")

def listdir(path ='.'):
    for file in os.listdir(path):
        print(os.path.join(path, file))


def main(argv):
    shell = FTPShell()
    shell.cmdloop()
    



if __name__ == "__main__":
    main(sys.argv[1:])
    