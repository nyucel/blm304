#BERAT KANAR


import socket
import time

 

msgFromClient       = "Client:Hello!"

bytesToSend         = str.encode(msgFromClient)

ip                  =input("Enter IP here: ")

serverAddressPort   = (ip, 42)

bufferSize          = 1024*15




 



s =socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 





choice  = input("Download or Upload (GET/PUT)? = ").encode()
s.sendto(choice,serverAddressPort)


Filename = input("File Name : ").encode()

s.sendto(Filename,serverAddressPort)

if( choice.decode() == "GET") :
        
        
        file = open(Filename , 'wb')
        file_data,serverAddressPort = s.recvfrom(bufferSize)
        try:
            while(file_data):
                print("Client:Downloading...")
                file.write(file_data)
                s.settimeout(2)
                file_data = s.recvfrom(bufferSize)
        except:
            print("Client:File has been downloaded..Program will be terminated in 5 seconds.")
            time.sleep(6)
            s.close()
            file.close()
            
        
elif (choice.decode() == "PUT") :
        
        file = open(Filename.decode() , 'rb')
        file_data = file.read(bufferSize)
        
        
        while(file_data):
            if(s.sendto(file_data,serverAddressPort)):
                file_data = file.read(bufferSize)
                print("Client:Sending...")
        print("Client:File has been uploaded..Program will be terminated in 5 seconds.")
        time.sleep(6)
        s.close()
        file.close()    
