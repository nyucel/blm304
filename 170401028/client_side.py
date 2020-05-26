import socket
from sys import exit
import os
import datapacket
import pickle


class Client:
    """"""

    def __init__(self, SERVER_IP="127.0.0.1", SERVER_PORT=42, BUFFERSIZE=5120):
        self.SERVER_IP = SERVER_IP
        self.SERVER_PORT = SERVER_PORT
        self.BUFFERSIZE = BUFFERSIZE
        self.PATH = os.path.abspath(os.getcwd())

        self.server_address = (SERVER_IP, SERVER_PORT)  ##ip&port çifti
        self.ClientSocket = None
        self.isConnected = False

        self.create_socket()  ## client udp socket oluştur
        self.CONNECT()  ## Bağlan
        self.LISTEN_USER()

    def create_socket(self):
        """Client side UDP Socketi oluşturur"""
        self.ClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        print("Client Side UDP socket oluşturuldu")

    def CONNECT(self):
        """SUNUCUYA GÖNDERİLEN İLK İSTEK
        AUTH Commandına sahip bir paket yolluyoruz, sunucu onaylarsa 230 cevabı döndürüyor,
        İleride buraları geliştirebilirim
        isconnected değerini true işaretliyoruz. """

        try:
            server_response = self.create_and_send_packet(command="AUTH")

            if (server_response == "230"):
                self.isConnected = True
                print("Bağlantı kuruldu")
            else:
                print("Bağlantı kurulamadı")

        except:
            print("Sunucuya mesaj yollama sırasında bir hata meydana geldi.. Sunucu ayakta mı ? ip doğru mu?")

    def LIST(self):
        """Sunucuda bulunan dosyaların listesi için istek yapan fonksiyon
        Serverside da NLST fonksiyonunu tetikler"""
        server_response = self.create_and_send_packet(command="NLST")
        print(server_response)

    def GET(self, filename):
        """Serverside RETR fonksiyonunu çalıştırıyor
        Sunucudan dosya indirme
        filename = > clientte bulunan dosyanınadı"""
        server_response = self.create_and_send_packet(command="RETR", data=filename)
        file_path = self.PATH + "\\clientside_folder\\" + filename  # dosyanın yazılacağı konum
        if not self.isConnected:
            print("Herhangi bir sunucuya bağlı değilsiniz.")
            return

        if (os.path.exists(file_path) == True):  # aynı isimde dosya varsa
            print("Bu dosya zaten clientside folder' da var.")
            return

        if server_response == "530":
            print("Sunucu kimliği doğrulayamamış")
            return

        if server_response == "452":
            print("Bu dosya sunucuda yok ya da adı yanlış girilmiş")
            return

        # error code dönmediyse almaya başlıyoruz.
        print("Yükleme başlıyor")
        try:
            f = open(file_path, "wb")
            while True:
                data = self.listen_and_return_file_data()
                packet_data = data[0]
                packet_sequenceNumber = data[1]

                if packet_sequenceNumber == -1 : break

                f.write(packet_data)

            self.check_file_integrity(server_response.data, server_response.checksum)
            print("Dosya Karşıdan yüklendi")
            f.close()
        except:
            print("Dosya karşıdan  yüklenirken bir hata oluştu.")

    def PUT(self, filename):
        """Serverside STOR fonksiyonunu çalıştırıyor,
        Sunucuya dosya yükleme
        filename = > yüklenecek dosyanın adı"""
        print("Lütfen yüklemek istediğiniz dosyanın kullanılmadıgından(açık olmadıgından) emin  olun... ")
        file_path = self.PATH + "\\clientside_folder\\" + filename  ## yazılacak dosya yolu

        if (os.path.exists(file_path) == False):  ## sende yüklemek istediğin dosya yoksa
            print("Böyle bir dosyanın clientside_folder dosyası içinde bulunduğundan emin olun")
            return

        #dosya adını yolluyuoruz
        server_response_1 = self.create_and_send_packet(command="STOR", data=filename)

        if server_response_1 == "553":
            print("Bu isimde bir dosya serverde yüklü..")
            return

        if server_response_1 == "500":
            print("Sunucu tarafında bilinmeyen bir hata meydana geldi..")
            return

        if server_response_1 == "150":
            print("Dosya karşıda oluşturuldu.. içerik yollanıyor")

            f = open(file_path, "rb")
            f_data = f.read()
            print(f_data)
            server_response_2 = self.create_and_send_packet(command="DATA", data=f_data)
            if (server_response_2 == "200"):
                print("Dosya sunucuya yüklendi.")
            else:
                print("Başarısız..")
        else:
            print("Başarısız.")

    def TEST(self, echo):
        """Sunucuya yollanan mesajı yankılandırır."""
        server_response = self.create_and_send_packet(command="TEST", data=echo)
        print(" Sunucunun cevabı : " + server_response.data)

    def ABORT(self):
        """Bu fonksiyon çalıştıktan sonra dosya indirme,yükleme,güncelleme
        işlemlerine server tarafındanizin verilmiyor"""

        server_response = self.create_and_send_packet(command="QUIT")

        if server_response == "231":
            print("Sunucu bağlantısı kesildi.")
            isConnected = False
        else:
            exit("Bağlantı kesilemedi program kapanıyor")

    def check_file_integrity(self, data, checksum):
        """Karşıdan yüklenen veriyinin checksum değerini hesaplıyoruz,
        server tarafından yollanan checksum değeri ile eşitse doğrulanmış oluyor"""
        dp = datapacket.DataPacket("", 0, "")
        if checksum == dp.calculateChecksum(data):
            print("Dosya içeriği kontrol edildi ! OK")
            return True
        else:
            print("Dosya düzgün iletilememiş ! X")
            return False

    def LIST_CLIENT_FILES(self):
        files_in_directory = os.listdir('clientside_folder')
        text = ""
        if len(files_in_directory) == 0:
            print("Yerelde hiç dosya yok.")
            return

        for i in range(len(files_in_directory)):
            text += str(i + 1) + " . " + str(files_in_directory[i]) + "\n"
        print((text))

    def create_and_send_packet(self, command="", seqNumber=0, data=""):
        """Verilen parametreler ile Sunucuya UDP paketi yolluyor,
        sunucudan dönen cevabı return ediyor
        """

        ## YOLLA 

        datapckt = datapacket.DataPacket(command, seqNumber, data)
        pickled_datapacket = pickle.dumps(datapckt)
        self.ClientSocket.sendto(pickled_datapacket, self.server_address)

        ## CEVABI DÖNDÜR
        server_response = self.ClientSocket.recvfrom(self.BUFFERSIZE)[0]
        try:
            ## encoded 
            response_data = server_response.decode(encoding="UTF-8")
            return response_data

        except:
            ## pickled ise
            response_data = pickle.loads(server_response)
            return response_data

    def listen_and_return_file_data(self):
        """server veri akıtırken her bir veri paketini çözen fonksiyon"""
        server_response = self.ClientSocket.recvfrom(self.BUFFERSIZE)[0]

        server_response = pickle.loads(server_response)

        return ((server_response.data, server_response.seqNumber)) ## veri ve sıra numarasını dönüyoruz.

    def LISTEN_USER(self):
        try:
            while (self.isConnected == True):
                print("""
                    Yapmak istediğiniz işlemi seçin
                    1. Yerelimdeki dosyaları listele
                    2. Sunucudaki dosyaları listele
                    3. Sunucu ile bağlantıyı test et
                    4.Sunucuya dosya yükle 
                    5. Sunucudan dosya indir
                    6.Sunucu ile bağlantıyı kes
                    1-2-3-4-5-6 gibi seçim yapın""")

                choice = int(input())
                if choice == 1:
                    self.LIST_CLIENT_FILES()
                elif choice == 2:
                    self.LIST()
                elif choice == 3:
                    self.TEST(input("Sunucuya bir şey yazın mesela ' Selam '"))
                elif choice == 4:
                    self.PUT(input("YÜklemek istediğiniz dosyanın adını giriniz"))
                elif choice == 5:
                    self.GET(input("Sunucudan indirmek istediğiniz dosya adını girin."))
                elif choice == 6:
                    self.ABORT()
                else:
                    print("Böyle bir seçim yok")
        except:
            print("İstemci çalışmayı durdurdu.")


# IP = input("Bağlanmak istediğiniz sunucunun IP adresini giriniz.")
# PORT = int(input("Bağlanmak istediğiniz PORT numarasını giriniz"))
c = Client(SERVER_IP="127.0.0.1", SERVER_PORT=42)
