import socket
import os
import sys

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverIp = input("Enter the IP address of the server:")
serverAddress = (serverIp, 42)
bufferSize=1024

listele = "lst"
sendListele = listele.encode('utf-8')
try:
    clientSocket.sendto(sendListele, serverAddress)

except:
    print('connection error')
    sys.exit()

message, addr = clientSocket.recvfrom(bufferSize)
sendMessage = message.decode('utf-8')
newMessage = "List of files in server:{}".format(sendMessage)
print(newMessage)

request = input("For receiving file from server: get file_name\nFor sending file to server: put file_name\n")
sendRequest = request.encode('utf-8')
clientSocket.sendto(sendRequest, serverAddress)  #istek gönderildi

if (request.find('get') == 0):

    fileTransfer,adress = clientSocket.recvfrom(bufferSize)
    if (fileTransfer.decode('utf-8') == 'notFound'):
        print('File is not found')
    else:
        f = open(fileTransfer.strip(), 'wb')
        fileTransfer,adress = clientSocket.recvfrom(bufferSize)
        try:
            while (fileTransfer):
                fileTransfer,adress = clientSocket.recvfrom(bufferSize)
                f.write(fileTransfer)
                clientSocket.settimeout(1)
        except socket.timeout:
            f.close()
        clientSocket.sendto(b'ISSUCCESS', serverAddress)
        clientSocket.close()

elif(request.find('put') == 0):
    fileList = os.listdir()
    if request[4:] in fileList:
        file = request[4:].encode('utf-8')
        f = open(request[4:], "rb")
        putFile = f.read(1024)
        clientSocket.sendto(file, serverAddress)     #dosya adı gönderildi
        clientSocket.sendto(putFile, serverAddress)   #dosya icerigi
        try:
            clientSocket.settimeout(1)
            data,adress = clientSocket.recvfrom(bufferSize)
            isPut = data.decode('utf-8')
            if (isPut == 'SUCCESS'):
                print('Successfull!  File submission is completed.')

        except socket.timeout:
            print('error')
        f.close()
        clientSocket.close()
    else:
        print('file is not found')
        sys.exit()
else:
    print('Bad Request')