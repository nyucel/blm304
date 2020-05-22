import socket
import os
import pickle ## pickle ile bir nesneyi transfer edebiliyorum
import datapacket ## Paketimizin data kısmı 
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
    
    
    def send_msg_to_client(self,message,clientAdress):
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
            """ Clientden gelen mesajı okuyacağım ve datanın command değerine göre
            belirli fonksiyonlara tabi tutulacak """
            try:
                client_msg = self.ServerSocket.recvfrom(self.BUFFERSIZE)
                
                data =client_msg[0]## data
                address = client_msg[1] ## ip&port
                data = pickle.loads(data) ## datayı çözüp datapacket tipine getiriyoruz.
                
                if(data.command == "AUTH"): ## BAĞLANTI KUR
                    self.AUTH(address)
                    continue
                    
                if(data.command == "NLST"): ## SUNUCUDA BULUNAN DOSYALARI LISTELE(LS)
                    self.NLST(address)
                    continue
            
                if(data.command == "STOR"): ## SUNUCUYA DOSYA YUKLE(PUT)
                    self.STOR(data,address)
                    continue

                if(data.command == "RETR"): ## SUNUCUDAN DOSYANIN BIR KOPYASINI YERELİNE İNDİR(GET)
                    self.RETR(data,address)
                    continue

                send_msg_to_client("501 SYNTAX HATASI ? SERVER BU KOMUTU BULAMADI")
                
            except:
                send_msg_to_client("500-* ? KOMUT İŞLETİLEMEDİ VEYA BİR HATA OLUŞTU")
                
                
    
            
    def AUTH(self,address):
        """Client Baglandıgı zaman dict'e ekleniyor baglama sırasında herhangi bir 
        kimlik denetimi yapılmıyor ileride belki bir güvenlik mekanizması olabilir.
        
        ip adresi ve port numarasını dict e ekledim ve True olarak işaretledim. 
        İlerideki işlemlerde IP adresinin kayıtlı olup olmadığını kontrol edeceğim."""
        try:
            self.connectedClientDict[address] = True
            self.send_msg_to_client("230 LOGGED IN ",address)
            
        except:
            self.send_msg_to_client("530 NOT LOGGED IN",address)
            
            
            
        
        print("yeni bağlantı var.")
        

        
    def NLST(self,address):
        """DIZINDEKİ DOSYALARI CLIENTE YOLLAYACAK FONKSIYON"""
        """Önce dosyaları listeledim, sonra kullanıcıya yollanabilecek düzgün görünümlü bir text oluşturdum"""
        """Sonra o texti kullanıcıya yolladım."""
        try:
            files_in_directory = os.listdir('serverside_folder') 
            text = ""
        
            for i in range(len(files_in_directory)): 
                text += str(i+1) + " . " + str(files_in_directory[i]) + "\n"
            
            self.send_text_msg(text,address)
            
            self.send_text_msg("212",address)
            
        except:
            
            self.send_msg_to_client("502",adress)
             
        
        
        
    
    def RETR(self,data,address):
        """
        CLIENTE DOSYAYI GONDEREN FONKSIYON
        address parametresi = > CLİENT'in adresi
        data parametresi = > dosya adı ve ek veri
        
        önce böyle bir dosyanın bulunup bulunamadığınına bakalım,
        ardından dosyanın içeriğinin buffer değerini aşıp aşmadığına bakalım, aşıyorsa 
        """
        try:
            file_path = self.PATH + "\serverside_folder\\" + data.data ## istenilen dosyanın konumu
            
            if(path.exists(file_path) == False): ## öyle bir dosya yoksa
                send_msg_to_client("550 Dosya bulunamadı ?")
                return
            
            if(os.path.getsize(file_path) < self.BUFFERSIZE): ## dosyanın içeriği bufferden küçükse yolluyoruz
                ## burada yolla
                pass
                
        except:
            send_msg_to_client("502",address)
            
            
        
    
    def STOR(self):
        pass
            
    
s = FTPServer()
