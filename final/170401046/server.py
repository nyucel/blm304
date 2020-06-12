import socket
import sys
import time
server_address = ("127.0.0.1", 142)
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind(server_address)

server_sock.listen(1)

conn, addr = server_sock.accept()
print('Connected by', addr)
while True:

    try:
        data = conn.recv(1024)

        if not data: break
        print(data)
        milliseconds = str(round(time.time() * 1000))
        time_period = " UTC+3"
        time = milliseconds + time_period
        A = time.encode("utf-8")
        conn.send(A)

    except socket.error:
        print ("Error Occured.")
        break

conn.close()




