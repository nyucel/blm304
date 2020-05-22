Running the server:
===================

To start the server just run the start_server.py file in the server directory.
The same way to stop the server just run the stop_server in the server directory.

Connect to the server:
======================

To connect to the server you should find in the client directory a file named
myftp.py, just run the file as follows:

./myftp.py -p PORT -r REMOTE

where PORT is the port number and REMOTE is the ip address of the server.

Note:
-----

Default port=42 and ip = 127.0.0.1 (localhost).
You may need root access run the server to listen on port 42.

