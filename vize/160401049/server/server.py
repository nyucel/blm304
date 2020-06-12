#Melis GULER
#160401049
import socket
import os

serverIp = 'localhost'
port = 42
address=(serverIp, port)

while (1):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # baglanti tipi udp olarak ayarlandi
    serverSocket.bind(address)
    print("Server initiliazed... ")
    print("Client waitinig... ")
    command, addr= serverSocket.recvfrom(1024)
    cmd = command.decode()

    method= cmd[:3]
    content= cmd[4:]

    if (method == 'get'):

            files = os.listdir()
            if content in files:
                fileName = content.encode('utf-8')
                f = open(content, "rb")
                fileTransfer = f.read(1024)
                serverSocket.sendto(fileName, addr)
                serverSocket.sendto(fileTransfer, addr)
                try:
                    serverSocket.settimeout(1)
                    transfer, adress = serverSocket.recvfrom(1024)
                    transferSuccess = transfer.decode('utf-8')
                    if (transferSuccess == 'ISSUCCESS'):
                        print('Successfull! File submission is completed.')
                        break
                except socket.timeout:
                    print('error')
                f.close()
                serverSocket.close()
            else:
                serverSocket.sendto(b'notFound', addr)
                serverSocket.close()

    elif (method == 'put'):

            msg, adrr = serverSocket.recvfrom(1024)
            data = msg.decode('utf-8')
            f = open(data.strip(), 'wb')
            message,adrr = serverSocket.recvfrom(1024)
            try:
                while (message):
                    message,adrr = serverSocket.recvfrom(1024)
                    f.write(message)
                    serverSocket.settimeout(1)
            except socket.timeout:
                f.close()
            serverSocket.sendto(b'SUCCESS', addr)
            serverSocket.close()

    elif (method == "lst"):
        fileList = str(os.listdir())
        sendFileList = fileList.encode('utf-8')
        serverSocket.sendto(sendFileList, addr)