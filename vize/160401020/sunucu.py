import socket   # Import socket module
import os
import pathlib

#MUCAHİD TAM 160401020

ftp_path = str(pathlib.Path(__file__).parent.absolute()) + "/ftp/"

if not os.path.exists(ftp_path):
    os.makedirs(ftp_path)


localIP='0.0.0.0'
localPort=42

UDPServerSocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

print('UDP Server listening from ip ' + localIP)

while True:
    msglis, address = UDPServerSocket.recvfrom(1024) 
    print ('Connection Accepted From', address)
    
    msglis = msglis.decode('utf-8')
    ftp_type = msglis.split(',')[0]

    if ftp_type == 'GET':
        filename = msglis.split(',')[1]
        if os.path.isfile(ftp_path+filename):
            print("FILE FOUND..!")
        else:
            print("FILE NOT FOUND..!")
            continue

        print ("sending file")

        UDPServerSocket.sendto(("PUT," + filename).encode('utf-8'), address)

        with open(ftp_path+filename,'rb') as f:
            l = f.read(1024)
            while (l):
                UDPServerSocket.sendto(l, address)
                l = f.read(1024)
            UDPServerSocket.sendto("!!FINISHED!!".encode(), address)

        print ("file sent")

    elif ftp_type == 'PUT':
        filename = msglis.split(',')[1]
        f = open(ftp_path+filename,'wb')      #open that file or create one
        l, address = UDPServerSocket.recvfrom(1024)         #get input
        print ("Receiving...File Data")

        try:
            while (l):
                try:
                    if len(l) < 15 and l.decode() == "!!FINISHED!!":       #get again until done
                        break;
                except:
                    continue
                f.write(l)            #save input to file
                l, address = UDPServerSocket.recvfrom(1024)

            print ("Received...File Data")
            f.close()
        except:
            print ("Receiving file is failed!!!")
    elif ftp_type == 'LIST':
        dir_list = os.listdir(ftp_path)
        UDPServerSocket.sendto(str(dir_list).encode(), address)
        print (dir_list)