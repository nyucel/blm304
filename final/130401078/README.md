# Start the Server from server directory

#### Start the server with default TIMEZONE="UTC+3"

sudo ./start_server.py
======================

#### Or start the server with a specific timezone 

sudo ./timeserver.py --timezone UTC-2 --start 
=============================================

# Stop the server from server directory

sudo ./stop_server.py 
=====================
 or 
 
sudo ./timeserver.py --stop
===========================


# Running the Client from client directory


sudo ./ntpclient.py  -r HOST -p PORT
====================================

HOST defaults to 127.0.0.1

PORT defaults to 142
