#Onur Karabulut 170401076
import socket
import datetime

sct = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = ""
port = 142
buf = 1024
UTC = "UTC+3" # UTC degeri buradan degistirilebilir
sct.bind((host, port))
sct.listen(1)


while True:
	connection, who = sct.accept()
	print("Baglanan Istemci IP: {0}".format(who[0]))  
	time_now = datetime.datetime.now().timestamp() * 1000
	time_now_utc = str(time_now) + "  " + UTC
	connection.send(time_now_utc.encode())   
sct.close()
     
    
