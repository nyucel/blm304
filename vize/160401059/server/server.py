#BERAT KANAR 


import socket
import os
import time





#path = "C:\\Users\\Casper\\Desktop\\server2"






localIP     = "127.0.0.1"

localPort   = 42

bufferSize  = 1024*15

 

msgFromServer       = "Server:Hello!"

bytesToSend         = str.encode(msgFromServer)

 


s =socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) #Socket olusturuldu.


s.bind((localIP, localPort)) #Verilen ip ve portu dinliyor.

 

print("Server is up and listening..")

def get(fileName):                         #Sunucudan dosya indirmek için fonksiyon.
        file = open(fileName , 'rb')
        file_data = file.read(bufferSize)
        while(file_data):   
            if(s.sendto(file_data,address)):
                print("Server:sending...")
                file_data = file.read(bufferSize)
              
        print("Server:File has been uploaded...")
        time.sleep(6)  
        s.close()
        file.close()
def put(fileName):                                                      #Sunucuya dosya yüklemek için gerekli fonksiyon.
        file = open(fileName , 'wb')                              
        file_data,serverAddressPort = s.recvfrom(bufferSize)
        #file_data = s.recvfrom(bufferSize)[0]
        try :
            while(file_data):
                print("Server:Downloading...")
                file.write(file_data)
                s.settimeout(2)
                file_data = s.recvfrom(bufferSize)
           
        except socket.timeout:
            print("Server:File has been downloaded..Program will be terminated in 5 seconds.")
            time.sleep(6)
            s.close()
            file.close()
                    





while(True):
    choice = s.recvfrom(bufferSize)[0].decode()
    
    bytesAddressPair = s.recvfrom(bufferSize)

    fileName = bytesAddressPair[0]

    address = bytesAddressPair[1]


    
    if(choice == "GET"):
        #files = os.listdir(path)
        #for name in files:
            #print(name)
        
        get(fileName)
    
        
    
    else:
        
        put(fileName) 
        
    
    
    

