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
        self.connectedClientDict = {("127.0.0.1",7000):False} ## Bağlı client adresleri, True ise işlem yapabilir.
        
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
            
            client_msg = self.ServerSocket.recvfrom(self.BUFFERSIZE)
            
            data =client_msg[0]## data
            address = client_msg[1] ## ip&port
            data = pickle.loads(data) ## datayı çözüp datapacket tipine getiriyoruz.
            
            print(data.command)
            if(data.command == "AUTH"): ## BAĞLANTI KUR
                self.AUTH(address)
                continue
                
            if(data.command == "NLST"): ## SUNUCUDA BULUNAN DOSYALARI LISTELE(LS)
                self.NLST(address)
                continue
        
            if(data.command == "STOR"): ## SUNUCUYA DOSYA YUKLE(PUT)
                self.STOR(address,data)
                continue

            if(data.command == "RETR"): ## SUNUCUDAN DOSYANIN BIR KOPYASINI YERELİNE İNDİR(GET)
                self.RETR(data,address)
                continue
            
            if(data.command == "QUIT"): ## Kullanıcının adresini dict den çıkart
                self.QUIT(address)
                continue
            
            if(data.command == "TEST"):
                self.TEST(address,data)
                continue
                
            
                
                
    
            
    def AUTH(self,address):
        """Client Baglandıgı zaman dict'e ekleniyor baglama sırasında herhangi bir 
        kimlik denetimi yapılmıyor ileride belki bir güvenlik mekanizması olabilir.
        
        ip adresi ve port numarasını dict e ekledim ve True olarak işaretledim. 
        İlerideki işlemlerde IP adresinin kayıtlı olup olmadığını kontrol edeceğim."""
        try:
            self.connectedClientDict[address] = True
            self.send_msg_to_client("230",address)
            
        except:
            self.send_msg_to_client("530",address)
            
            
            
        
        print("yeni bağlantı var.")
        

        
    def NLST(self,address):
        """DIZINDEKİ DOSYALARIN ADLARINI CLIENTE YOLLAYACAK FONKSIYON"""
        """Önce dosyaları listeledim, sonra kullanıcıya yollanabilecek düzgün görünümlü bir text oluşturdum"""
        """Sonra o texti kullanıcıya yolladım."""
        try:
            
            files_in_directory = os.listdir('170401028/serverside_folder') 
            text = ""
            if(len(files_in_directory) == 0):
                self.send_msg_to_client("Hiç dosya yüklenmemiş.",address)
                return
            
            for i in range(len(files_in_directory)): 
                text += str(i+1) + " . " + str(files_in_directory[i]) + "\n"
            
            self.send_msg_to_client(text,address)
            
            
            self.send_text_msg("212",address)
            
        except:
            self.send_msg_to_client("502",address)
             
        
        
        
    
    def RETR(self,data,address):
        """
        CLIENTE DOSYAYI GONDEREN FONKSIYON
        address parametresi = > CLİENT'in adresi
        data parametresi = > dosya adı ve ek veri
        
        önce client AUTH isteği yollamış mı ona bakalım.
        ardından böyle bir dosyanın bulunup bulunamadığınına bakalım,
        ardından dosyanın içeriğinin buffer değerini aşıp aşmadığına bakalım, aşıyorsa 
        """
        if(address not in self.connectedClientDict or self.connectedClientDict[address]==False): ## connect yollanmamış
            self.send_msg_to_client("530",address) 
            return
        try:
            file_name = data.data ## istenen dosyanın adı
            file_path = self.PATH + "\\170401028\\serverside_folder\\" + file_name ## istenilen dosyanın konumu
            
            if(os.path.exists(file_path)==False): ## istenilen dosya yoksa
                self.send_msg_to_client("452",address)
            
            f  = open(file_path,"r") 
            file_data = f.read()  ## dosyanın içini okuduk
            
            data_packet = datapacket.DataPacket("FILE",0,file_data)
            data_packet = pickle.dumps(data_packet)
            f.close()
            self.ServerSocket.sendto(data_packet,address)
        except:
            send_msg_to_client("450",address)
        
        
    
    def STOR(self,address,data):
        """Bu fonksiyon ile client servere dosya yüklüyor, bu fonksiyon iki fazda çalışacak
        ilk paket yollandığında clientin yollamak istediği dosya adında bir dosya oluşturulacak
        ikinci pakette client dosyanın içeriğini yollayacak."""
        try:
            if(address not in self.connectedClientDict or self.connectedClientDict[address]==False):
                self.send_msg_to_client("530",address) 
                return
            
            
            file_name  = data.data
            file_path = self.PATH + "\\170401028\\serverside_folder\\" + data.data
            
            if(os.path.exists(file_path) == True): ## böyle bir dosya zaten varsa
                self.send_msg_to_client("553",address)
                return

            f = open(file_path,"w") ## client dosyasını oluşturduk içeriğini clientten alıp doldurmalıyız.
            
            self.send_msg_to_client("150",address) ## cliente 150 ile işlemi devam ettirmesi gerektiğini söyledik
            
            client_msg = self.ServerSocket.recvfrom(self.BUFFERSIZE)
                
            data =client_msg[0]## data
            address = client_msg[1] ## ip&port
            
            data = pickle.loads(data) ## veriyi DataPacket haline dönüşütürdük
            
            f.write(data.data) ## DataPacket data kısmını dosyaya yazdık

            if(data.checksum == data.calculateChecksum(data.data)):
                self.send_msg_to_client("200",address)
            else:
                self.send_msg_to_client("600",address)
            
            f.close()
        except:
            send_msg_to_client("500",address)
        
        
    
    def TEST(self,address,data):
        """Servere yollanan datayı echo yapıyor, 
        paketlerin düzgün yollanıp yollanamadığını kontrol etmek için"""
        
        newP = datapacket.DataPacket("TEST",0,data.data)
        pickled_newP = pickle.dumps(newP)
        self.ServerSocket.sendto(pickled_newP,address)
    
    def QUIT(self,address):
        """Kullanıcının ip&port bilgisini dictionary den çıkartıyoruz
        Disconnect olmuş oluyor."""
        try:
            disconnected = self.connectedClientDict.pop(address)
            print(disconnected + "Adresli bağlantı disconnect oldu")
            self.send_msg_to_client("231",address)
        except:
            self.send_msg_to_client("500",address)
        
    def close_server_and_abort_program(self):
        """soketi kapa while döngüsünden çık"""
        self.ServerSocket.shutdown()
        self.ServerSocket.close()

s = FTPServer()


