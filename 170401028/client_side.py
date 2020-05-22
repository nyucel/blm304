import socket
import datapacket
import pickle
 

msgFromClient       = "AUTH"

bytesToSend         =  msgFromClient

serverAddressPort   = ("127.0.0.1", 42)

bufferSize          = 4096

 

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 

# Send to server using created UDP socket

UDPClientSocket.sendto(bytesToSend, serverAddressPort)


 

msgFromServer = UDPClientSocket.recvfrom(bufferSize)

 

msg = "Message from Server {}".format(msgFromServer[0])

print(msg)


