# Start the Server

#### Start the server with default TIMEZONE="UTC+3"

sudo ./start_server.py
======================

#### Or start the server with a specific timezone 

sudo ./timeserver.py --timezone UTC-2 --start 
=============================================

# Stop the server

sudo ./stop_server.py 
=====================
 or 
 
sudo ./timeserver.py --stop
===========================


# Running the Client


sudo ./ntpclient.py  -r HOST -p PORT
====================================

HOST defaults to 127.0.0.1

PORT defaults to 142
