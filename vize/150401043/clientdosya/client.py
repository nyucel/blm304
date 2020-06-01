#mustafa akbulut
import socket
import time
import sys

UDP_IP = sys.argv[2]
UDP_PORT = 42
buf = 1024
file_name = sys.argv[1]
com = sys.argv[3]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(com.encode('utf-8'), (UDP_IP, UDP_PORT))

if(com == "put"):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(file_name.encode('utf-8'), (UDP_IP, UDP_PORT))
    print ("Sending %s ..." % file_name)

    f = open(file_name, "rb")
    data = f.read(buf)
    while(data):
        if(sock.sendto(data, (UDP_IP, UDP_PORT))):
            data = f.read(buf)
            time.sleep(0.02) # Give receiver a bit time to save

    sock.close()
    f.close()

if (com == "get"):
    while True:
        data, addr = sock.recvfrom(1024)
        if data:
            print ("File name:", data)
            file_name = data.strip()

        f = open(file_name, 'wb')

        while True:
            ready = select.select([sock], [], [], timeout)
            if ready[0]:
                data, addr = sock.recvfrom(1024)
                f.write(data)
            else:
                print ("%s Finish!" % file_name)
                f.close()
                break

