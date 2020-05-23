import socket
import datapacket
import pickle
 

class Client:
    """"""
    def __init__(self,SERVER_IP="127.0.0.1", SERVER_PORT=42, BUFFERSIZE = 4096):
        self.SERVER_IP = SERVER_IP
        self.SERVER_PORT = SERVER_PORT
        self.BUFFERSIZE = BUFFERSIZE
        
        self.server_address = (SERVER_IP,SERVER_PORT) ##ip&port çifti
        self.ClientSocket = None
        self.isConnected = False
        
        self.create_socket()
        self.CONNECT()
        self.GET("sample")
        
    def create_socket(self):
        """Client side UDP Socketi oluşturur"""
        self.ClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        print("Client Side UDP socket oluşturuldu")
    
    
    def CONNECT(self):
        """SUNUCUYA GÖNDERİLEN İLK İSTEK
        AUTH Commandına sahip bir paket yolluyoruz, sunucu onaylarsa 230 cevabı döndürüyor,
        isconnected değerini true işaretliyoruz. """
        
        try:
            server_response = self.create_and_send_packet(command="AUTH")
         
            if(server_response == "230" ):
                self.isConnected = True
                print("Bağlantı kuruldu")
            else:
                print("Bağlantı kurulamadı")
                
        except:
            print("Sunucuya mesaj yollama sırasında bir hata meydana geldi..")
            
    def LIST(self):
        """Sunucuda bulunan dosyaların listesi için istek yapan fonksiyon
        Serverside da NLST fonksiyonunu tetikler"""
        server_response = self.create_and_send_packet(command="NLST")
        print(server_response)
    
    def GET(self,filename):
        server_response   = self.create_and_send_packet(command="RETR",data=filename)
        
        with open(filename, 'wb') as the_file:
            the_file.write(server_response.data)

    def TEST(self,echo):
        server_response = self.create_and_send_packet(command="TEST",data=echo)
        print(server_response.data)
    
    def create_and_send_packet(self,command = "" , seqNumber = 0 , data = "" , checksum = 0):
        """Verilen parametreler ile Sunucuya UDP paketi yolluyor,
        sunucudan dönen cevabı return ediyor
        Ctype değeri nasıl bir paket yollandığını belirtiyor,
        """
        
        ## YOLLA 
        
        datapckt = datapacket.DataPacket(command,seqNumber,data,checksum)
        pickled_datapacket = pickle.dumps(datapckt)
        self.ClientSocket.sendto(pickled_datapacket,self.server_address)
        
        ## CEVABI DÖNDÜR
        server_response = self.ClientSocket.recvfrom(self.BUFFERSIZE)[0]
        try:
            ## encoded ise 
            response_data = server_response.decode(encoding = "UTF-8")
            return response_data
        
        except:
            ## pickled ise
            response_data  = pickle.loads(server_response)
            return response_data
            
            
        
c = Client()
