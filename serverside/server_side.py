import socket
import os
from time import sleep ## bunu import etmemin sebebi bir şeyler  hızlı oluyor ve bir şey iki üç kere yapılıyor
class FTPServer:
    
    def __init__(self,ip = "127.0.0.1", port = 42, timeout = 3, bufferSize = 4096):
        """Serverim için gerekli olacak değişkenleri ayarlıyorum"""
        self.UDP_IP = ip  
        self.UDP_PORT = port  
        self.SERVER_TIMEOUT = timeout  
        self.BUFFERSIZE = bufferSize 
        self.PATH = os.path.abspath(os.getcwd())  ## bulunduğum dizin
        
        
        self.ServerSocket = None  ## socket daha initialize edilmemiş
        self.connectedClientDict = {("127.0.0.1",7000):False} ## Bağlı client adresleri, True ise yetkili
        
        ##İnstance oluşturulduğu anda socket oluşturup dinlenmeye başlıyor.
        self.create_socket()
        self.listen()
    
    
    def send_msg(self,message,clientAdress):
        """Client'e mesaj gönderme"""
        if(self.ServerSocket == None ):        
            print("Server Socket Oluşturulmamış mesaj gönderilemedi")
            return
        try:
            self.ServerSocket.sendto(str.encode(message),clientAdress)
            print("Mesaj gönderildi..")
        except:
            print("Mesaj gönderimi sırasında herhangi bir hata oluşmuş olabilir.")
            
        
    
    
    def create_socket(self):
        """Server Socketi oluşturur ve ip&port bind eder"""
        self.ServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.ServerSocket.bind((self.UDP_IP, self.UDP_PORT))
        print("UDP Server oluşturuldu")
    
    def listen(self):
        while(True):
            """ Clientden gelen mesajı okuyacağım  ve 
            yolladığı mesaja göre belirli fonksiyonlara tabi tutulacak """
            
            client_msg = self.ServerSocket.recvfrom(self.BUFFERSIZE)
            
            message =client_msg[0].decode(encoding = 'UTF-8',errors = 'strict')  ## data

            address = client_msg[1] ## ip&port

            if(message == "CONNECT"):
                self.CONNECT(address)
                
            
            if(message == "LIST"):
                self.LIST(address)
                
    
    def CONNECT(self,address):
        """Client Baglandıgı zaman dict'e ekleniyor baglama sırasında herhangi bir 
        kimlik denetimi yapılmıyor ileride belki bir güvenlik mekanizması olabilir.
        
        ip adresi ve port numarasını dict e ekledim ve True olarak işaretledim. 
        İlerideki işlemlerde IP adresinin kayıtlı olup olmadığını kontrol edeceğim."""
        self.connectedClientDict[address] = True
        print("yeni bağlantı var.")
        

        
    def LIST(self,address):
        """DIZINDEKİ DOSYALARI CLIENTE YOLLAYACAK FONKSIYON"""
        """Önce dosyaları listeledim, sonra kullanıcıya yollanabilecek düzgün görünümlü bir text oluşturdum"""
        """Sonra o texti kullanıcıya yolladım."""
        
        files_in_directory = os.listdir('serverside/files') 
        text = ""
        
        for i in range(len(files_in_directory)): 
            text += str(i+1) + " . " + str(files_in_directory[i]) + "\n"
            
            
        self.send_msg(text,address) 
        
        
    
    def GET(self,message,address):
        """CLIENTE DOSYAYI GONDEREN FONKSIYON"""
        """DOSYA BUFFERDEN BÜYÜK İSE ÖNCE DOSYAYI PARÇALAMAK GEREKİYOR ARDINDAN POSTA POSTA YOLLAMALIYIZ."""
        pass
    
    def POST(self):
        pass
            
        
s = FTPServer()