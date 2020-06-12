#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date Fri Jun 12 01:32:14 2020
@author Abdoul Karim TOURE
@contact contact@trabdlkarim.com
@copyright Copyright 2020, Abdoul Karim TOURE
@license GPL v3.0 or Later
@version 1.0.1
@status Development
"""
import ctypes
import ctypes.util
import socket
import time
import argparse as arg
import sys
import os
from datetime import datetime
from datetime import timezone

HOST = "127.0.0.1"
PORT = 10020

NTP_DATA_PACKET ='0x1b' + 47*'\0' # Hex message to send to the server.


class NTPClient(object):
    def __init__(self,server_address):
        self.server_address = server_address
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def get_time(self):
        with self.socket:
            self.socket.connect(self.server_address)
            print("Sending NTP data packet...")
            self.start_tm = time.time()
            self.socket.sendall(bytes(NTP_DATA_PACKET+"\n","utf-8"))
            print("Retreiving time from ntp server...")
            received =  str(self.socket.recv(4096),"utf-8").strip('(,)').replace(" ","")
            self.localtime = received.split(',')
            self.localtime[0] = float(self.localtime[0])
            self.localtime[1] = self.localtime[1].strip("'")
            self.end_tm = time.time()

    def __set_limux_time(self,dtime):
        try:
            os.system("sudo timedatectl set-ntp false ")
            os.system("sudo date --set='%s' >> /dev/null " % dtime)
        except Exception as ex:
            print("FAILED: An error occured while setting system time. ")
            print(str(ex))



    def set_time(self):
        print("Setting system time...")
        delay = (self.end_tm - self.start_tm)/2
        timestamp = (self.localtime[0]/1000) + delay
        struct_time = time.gmtime(timestamp)
        dt = datetime.fromtimestamp(timestamp, timezone.utc)
        self.__set_limux_time(dt.strftime("%a  %b  %d %Y  %H:%M:%S "))
        print("Local time: ",end="")
        print(dt.strftime("%a  %b  %d %Y  %H:%M:%S ") + self.localtime[1])
        print("Time zone: " + self.localtime[1])
        print("System clock synchronized: Yes ")


    @staticmethod
    def parse_args(argv):
        parser = arg.ArgumentParser(prog="ntpclient",description="description: simple NTP client using TCP")
        parser.add_argument("-p","--port",type=int, default=PORT,help="server listening port")
        parser.add_argument("-r","--remote", default=HOST, help="remote host IP address ")
        parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0.1')
        args =  parser.parse_args(argv)
        args = vars(args)
        return args

class TimeSpecification(ctypes.Structure):
    _fields_ = [('tm_sec',ctypes.c_long),('tm_nsec',ctypes.c_long)]


def main(argv):
    args = NTPClient.parse_args(argv)
    ntp = NTPClient((args['remote'],args['port']))
    ntp.get_time()
    ntp.set_time()

if __name__=="__main__":
    main(sys.argv[1:])