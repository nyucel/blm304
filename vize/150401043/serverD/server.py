#mustafa akbulut
import socket
import select

UDP_IP = "127.0.0.1"
IN_PORT = 42 
timeout = 3


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, IN_PORT))
data, addr = sock.recvfrom(1024)

while True:
        data, addr = sock.recvfrom(1024)

if (data == "put"):
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
if (data == "get"):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(file_name.encode('utf-8'), (UDP_IP, UDP_PORT))
    print ("Sending %s ..." % file_name)

    f = open(file_name, "rb")
    data = f.read(buf)
    while(data):
        if(sock.sendto(data, (UDP_IP, UDP_PORT))):
            data = f.read(buf)
            time.sleep(0.02)

    sock.close()
    f.close()