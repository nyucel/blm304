#170401022 Cihan PAR
import socket
import datetime
import time

servertcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 142
servertcp.bind(("0.0.0.0", port))
print("Waiting for client respond.")
servertcp.listen(10)

while True:
    clienttcp, address = servertcp.accept()
    print("Client is connected.\nTime information is sending...")
    
    time_zone = 3  #UTC±x
    time_ms = (datetime.datetime.utcnow().timestamp()+time_zone*3600)*1000 #ms
    time_delay_ms_first = time.time_ns()
    if time_zone>=0:
        time_zone = "UTC+"+str("%02d" % time_zone)
    else:
        time_zone = "UTC"+str("%02d" % time_zone)
    clienttcp.sendall((str(time_ms)+","+time_zone).encode())
    message=clienttcp.recv(1024)
    print(message.decode())
    time_delay_ms_last = time.time_ns()
    time_delay_ms=(time_delay_ms_last-time_delay_ms_first)/1000000 #ms
    print("Delay = "+str(time_delay_ms)+" ms")
    clienttcp.sendall(str(time_delay_ms).encode())
    message=clienttcp.recv(1024)
    print(message.decode())