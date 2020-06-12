#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date Thu Jun 11 18:27:20 2020
@author Abdoul Karim TOURE
@contact contact@trabdlkarim.com
@copyright Copyright 2020, Abdoul Karim TOURE
@license GPL v3.0 or Later
@version 1.0.1
@status Development
"""

import os
import sys
import time
from datetime import datetime
from datetime import timezone
import argparse as arg
from socketserver import TCPServer
from socketserver import StreamRequestHandler

HOST = "127.0.0.1"
PORT = 10020

TIMEZONE = "UTC+3"   # Zaman dilimi degiskeni

GREEN = '\033[92m'
END = '\033[0m'

class TimeServerRequestHandler(StreamRequestHandler):
    def handle(self):
        self.data = self.rfile.readline().strip()
        print("Universal time: "+datetime.now(timezone.utc).isoformat(timespec='seconds'))
        print("time request from {} ".format(self.client_address))
        self.utc_timestamp = datetime.now(timezone.utc).timestamp()  # elapsed time since epoch in seconds
        self.tz_timestamp = int(TIMEZONE[3:]) * 3600  # timezone in seconds
        self.timedelta = self.utc_timestamp + self.tz_timestamp
        self.wfile.write(str((self.timedelta*1000,TIMEZONE)).encode())  # send time reponse in milliseconds

        print("Waiting for request.")

class NTPServer:
    def __init__(self,server_address, HandlerClass):
        self.server_address = server_address
        self.server = TCPServer(server_address, HandlerClass)

    def start_server(self):
        self.server_pid = os.getpid()
        with open("pid.txt","w") as pfile:
            pfile.write(str(self.server_pid)+"\n")
        print("Server starting...")
        print("Binding to address {}:{}...".format(HOST,PORT))
        time.sleep(2)
        print("Server is running on {}:{}".format(HOST,PORT))
        print("Active: service "+GREEN+"running"+END+" since %s" % datetime.now(timezone.utc).isoformat(timespec='seconds') )
        print("Server Timezone: "+TIMEZONE)
        print("Universal time: "+datetime.now(timezone.utc).isoformat(timespec='seconds'))
        print("Waiting for request.")
        with self.server:
            self.server.serve_forever()

    @staticmethod
    def stop_server():
        with open("pid.txt",'r') as pfile:
            pid = pfile.readline()
            pid = int(str(pid).strip())

        try:
            os.kill(pid,2)
            print("Server has been stopped.")
        except ProcessLookupError:
            print("Can't stop server, because it not running.")

    @staticmethod
    def parse_args(argv):
        parser = arg.ArgumentParser(prog="timeserver",description="description: simple NTP server using TCP protocol")
        group = parser.add_mutually_exclusive_group()
        global TIMEZONE
        global PORT
        parser.add_argument("-p","--port",type=int, default=PORT,
                            help="define the server's listening port")
        parser.add_argument("-t","--timezone", default=TIMEZONE,help="define the server's timezone")
        group.add_argument("--start", action='store_true', help="start the ntp server")
        group.add_argument("--stop",action="store_true", help="stop the ntp server  ")

        parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0.1')
        args =  parser.parse_args(argv)
        args = vars(args)
        PORT = args['port']
        TIMEZONE = args['timezone'].upper()
        return parser, args


def main(argv):

    parser, args = NTPServer.parse_args(argv)
    if args["start"] == True:
        try:
           server = NTPServer((HOST,args['port']), TimeServerRequestHandler)
           server.start_server()
        except (KeyboardInterrupt,SystemExit):

            print("\nServer stopped.")

    elif args["stop"] == True:
        NTPServer.stop_server()

    else:
        parser.print_help()

if __name__=="__main__":
    main(sys.argv[1:])