import socket
from sys import exit
import os
import datapacket
import pickle
 

class Client:
    """"""
    def __init__(self,SERVER_IP="127.0.0.1", SERVER_PORT=42, BUFFERSIZE = 4096):
        self.SERVER_IP = SERVER_IP
        self.SERVER_PORT = SERVER_PORT
        self.BUFFERSIZE = BUFFERSIZE
        self.PATH = os.path.abspath(os.getcwd())
        
        self.server_address = (SERVER_IP,SERVER_PORT) ##ip&port çifti
        self.ClientSocket = None
        self.isConnected = False
        
        self.create_socket() ## client udp socket oluştur
        self.CONNECT()  ## Bağlan
        self.LIST()
        
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
        """Serverside RETR fonksiyonunu çalıştırıyor
        Sunucudan dosya indirme
        filename = > clientte bulunan dosyanınadı"""
        server_response   = self.create_and_send_packet(command="RETR",data=filename)
        file_path =  self.PATH + "\\clientside_folder\\" + filename ## yollanacak  dosya yolu
        
        with open(file_path, 'w') as the_file:
            the_file.write(server_response.data)
        
        self.check_file_integrity(server_response.data,server_response.checksum)
        print("Dosya Karşıdan yüklendi")

    
    def PUT(self,filename):
        """Serverside STOR fonksiyonunu çalıştırıyor,
        Sunucuya dosya yükleme
        filename = > yüklenecek dosyanın adı"""
        file_path =  self.PATH + "\\clientside_folder\\" + filename ## yazılacak dosya yolu

        server_response_1 = self.create_and_send_packet(command="STOR",data=filename)
        
        if(server_response_1 == "553"):
            print("Bu isimde bir dosya serverde yüklü..")
            return
        elif(server_response_1 == "500"):
            print("Sunucu tarafında bilinmeyen bir hata meydana geldi..")
            return 
        elif(server_response_1 == "150"):
            print("Dosya karşıda oluşturuldu.. içerik yollanıyor")
            
            f  = open(file_path,"r")
            f_data = f.read(2048)
            
            server_response_2 =  self.create_and_send_packet(command="DATA", data = f_data)
            if(server_response_2 == "200"):
                print("Dosya sunucuya yüklendi.")
            else:
                print("Başarısız..")
        else:
            print("Başarısız.")
            
        
    

    def check_file_integrity(self,data,checksum):
        """Karşıdan yüklenen veriyinin checksum değerini hesaplıyoruz,
        server tarafından yollanan checksum değeri ile eşitse doğrulanmış oluyor"""
        dp = datapacket.DataPacket("",0,"")
        if(checksum == dp.calculateChecksum(data)):
            print("Dosya içeriği kontrol edildi ! OK")
            return True
        else:
            print("Dosya düzgün iletilememiş ! X")
            return False


    def TEST(self,echo):
        server_response = self.create_and_send_packet(command="TEST",data=echo)
        print(server_response.data)
    
    def ABORT(self):
        """Bu fonksiyon çalıştıktan sonra dosya indirme,yükleme,güncelleme
        işlemlerine server tarafındanizin verilmiyor"""
        
        server_response = self.create_and_send_packet(command="QUIT")
        
        if(server_response == "231"):
            print("Sunucu bağlantısı kesildi.")
            isConnected = False
        else:
            exit("Bağlantı kesilemedi program kapanıyor")
            
            
    def create_and_send_packet(self,command = "" , seqNumber = 0 , data = ""):
        """Verilen parametreler ile Sunucuya UDP paketi yolluyor,
        sunucudan dönen cevabı return ediyor
        """
        
        ## YOLLA 
        
        datapckt = datapacket.DataPacket(command,seqNumber,data)
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
