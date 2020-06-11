#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date Fri May 22 14:19:02 2020
@author Abdoul Karim TOURE
@contact contact@trabdlkarim.com
@copyright Copyright 2020, Abdoul Karim TOURE
@license GPL v3.0 or Later
@version 1.0.1
@status Development
"""



from ftpserver import myftpserver as server
import sys

def main(argv):
    server.main(argv)
    
if __name__ =="__main__":
    main(sys.argv[1:])

