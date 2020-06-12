import socket
import os
import pickle  ## pickle ile bir nesneyi transfer edebiliyorum
import datapacket  ## Paketimizin data kısmı
import time
import hashlib

# 170401028 - Emir Kıvrak

class FTPServer:

    def __init__(self, ip="127.0.0.1", port=42, bufferSize=65535, Chunksize=60000): ## sunucu adresi girilmezse localhost
        """Server için gerekli olacak değişkenleri ayarlıyorum"""
        self.UDP_IP = ip
        self.UDP_PORT = port
        self.BUFFERSIZE = bufferSize
        self.CHUNKSIZE = Chunksize  ## dosyalardan veriler bu büyüklükte okunup yollanacak
        self.PATH = os.path.abspath(os.getcwd())  ## bulunduğum dizin

        self.ServerSocket = None  ## socket daha initialize edilmemiş
        self.connectedClientDict = {("127.0.0.1", 7000): False}  ## Bağlı client adresleri, True ise işlem yapabilir.

        # bir nesne oluşturulduğunda dinlemeye başlıyor direk, böyle yapılmaya da bilir.

        self.create_socket()
        self.listen()

    def create_socket(self):
        """Server Socketi oluşturur ve ip&port bind eder"""
        self.ServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.ServerSocket.bind((self.UDP_IP, self.UDP_PORT))
        print("UDP Server oluşturuldu")



    def listen(self):
        while (True):
            """ Clientden gelen mesajı okuyacağım ve datanın command değerine göre
            belirli fonksiyonlara tabi tutulacak """

            client_msg = self.ServerSocket.recvfrom(self.BUFFERSIZE)

            data = client_msg[0]  # data
            address = client_msg[1]  # ip&port
            data = pickle.loads(data)  # datayı çözüp datapacket tipine getiriyoruz.

            print(data.command)
            if data.command == "AUTH":  # BAĞLANTI KUR
                self.AUTH(address)
                continue

            if data.command == "NLST":  # SUNUCUDA BULUNAN DOSYALARI LISTELE(LS)
                self.NLST(address)
                continue

            if data.command == "STOR":  # SUNUCUYA DOSYA YUKLE(PUT)
                self.STOR(address, data)
                continue

            if data.command == "RETR":  # SUNUCUDAN DOSYANIN BIR KOPYASINI YERELİNE İNDİR(GET)
                self.RETR(data, address)
                continue

            if data.command == "QUIT":  # Kullanıcının adresini dict den çıkart
                self.QUIT(address)
                continue

            if data.command == "TEST":
                self.TEST(address, data)
                continue

    def AUTH(self, address):
        """Client Baglandıgı zaman dict'e ekleniyor baglama sırasında herhangi bir 
        kimlik denetimi yapılmıyor ileride belki bir güvenlik mekanizması olabilir.
        
        ip adresi ve port numarasını dict e ekledim ve True olarak işaretledim. 
        İlerideki işlemlerde IP adresinin kayıtlı olup olmadığını kontrol edeceğim."""
        try:
            self.connectedClientDict[address] = True
            self.send_simple_msg_to_client("230", address)

        except:
            self.send_simple_msg_to_client("530", address)

        print("yeni bağlantı var.")

    def NLST(self, address):
        """DIZINDEKİ DOSYALARIN ADLARINI CLIENTE YOLLAYACAK FONKSIYON"""
        """Önce dosyaları listeledim, sonra kullanıcıya yollanabilecek düzgün görünümlü bir text oluşturdum"""
        """Sonra o texti kullanıcıya yolladım."""
        try:

            files_in_directory = os.listdir('serverside_folder')
            text = ""
            if (len(files_in_directory) == 0):
                self.send_simple_msg_to_client("Hiç dosya yüklenmemiş.", address)
                return

            for i in range(len(files_in_directory)):
                text += str(i + 1) + " . " + str(files_in_directory[i]) + "\n"

            self.send_simple_msg_to_client(text, address)

            self.send_text_msg("212", address)

        except:
            self.send_simple_msg_to_client("502", address)

    def RETR(self, data, address):
        """
        CLIENTE DOSYAYI GONDEREN FONKSIYON
        address parametresi = > CLİENT'in adresi
        data parametresi = > dosya adı
        
        önce client AUTH isteği yollamış mı ona bakalım.
        ardından böyle bir dosyanın bulunup bulunamadığınına bakalım,
        ardından dosyanın içeriğini paketler halinde cliente yollayalım,
        cliente dosya yollarken datanın sequencenNumber yani sıra numarası parametresini bir bir arttırıcaz.
        client dosyalar karışık halde gelmiş olsa bile onları bu sıra numarası ile sırayla dizebilecek
        Yolladığımız son veririnin  command değeri 200 olacak böylece client bunun son paket olduğunu anlayacak

        """
        if (address not in self.connectedClientDict or
                self.connectedClientDict[address] == False):  # connect yollanmamış
            self.send_simple_msg_to_client("530", address)
            return

        file_name = data.data  # istenen dosyanın adı
        file_path = self.PATH + "\\serverside_folder\\" + file_name  # istenilen dosyanın konumu

        if (os.path.exists(file_path) == False):  # istenilen dosya yoksa
            self.send_simple_msg_to_client("452", address)
        try:
            f = open(file_path, "rb")
            sequenceNumber = 0
            while True:
                file_data = f.read(self.CHUNKSIZE)  # dosyanın içini istenilen boyut kadar okuduk
                if not file_data: break

                self.send_datapacket_msg_to_client(address=address, command="FILE",
                                                   seqNumber=sequenceNumber, data=file_data)

                sequenceNumber += 1  # Paket numarasını bir artttırdık.
                print("Cliente " + str(sequenceNumber) + "Numaralı paket yollandı.")
                time.sleep(0.04)  # karşının karşılayıp yazması için bir zaman veriyoruz.
            f.close()
            print("Tüm veri paketler  yollandı.")

            # son pakette data kısmında yolladığımız tüm verinin özet değerini yolluyoruz.

            self.send_datapacket_msg_to_client(address=address, command="200",
                                               seqNumber=-1, data=self.md5(file_path))
        except:
            self.send_datapacket_msg_to_client(address=address, command="500", seqNumber=-99)

    def STOR(self, address, data):
        """Bu fonksiyon ile client servere dosya yüklüyor, bu fonksiyon iki fazda çalışacak
        ilk paket yollandığında clientin yollamak istediği dosya adında bir dosya oluşturulacak
        ikinci pakette client dosyanın içeriğini yollayacak."""

        if (address not in self.connectedClientDict or self.connectedClientDict[address] == False):
            self.send_simple_msg_to_client("530", address)
            return
        file_name = data.data
        file_path = self.PATH + "\\serverside_folder\\" + data.data

        if (os.path.exists(file_path) == True):  # böyle bir dosya zaten varsa
            self.send_simple_msg_to_client("553", address)
            return

        f = open(file_path, "wb")  # client dosyasını oluşturduk içeriğini clientten alıp doldurmalıyız.

        self.send_simple_msg_to_client("150", address)  # cliente 150 ile işlemi devam ettirmesi gerektiğini söyledik

        data = ""
        while True:
            client_msg = self.ServerSocket.recvfrom(self.BUFFERSIZE)

            data = client_msg[0]  # data

            data = pickle.loads(data)  # veriyi DataPacket haline dönüşütürdük
            print(data.command)

            if data.command == "END": break

            f.write(data.data)  # DataPacket data kısmını dosyaya yazdık

        f.close()

        if data.data == self.md5(file_path):
            self.send_simple_msg_to_client("200", address)
        else:
            self.send_simple_msg_to_client("600", address)

    def TEST(self, address, data): 
        """Servere yollanan datayı echo yapıyor, 
        paketlerin düzgün yollanıp yollanamadığını kontrol etmek için"""

        self.send_datapacket_msg_to_client(address=address, command="TEST", data=data.data)
        print(data.data)

    def QUIT(self, address):
        """Kullanıcının ip&port bilgisini dictionary den çıkartıyoruz
        Disconnect olmuş oluyor."""
        try:
            disconnected = self.connectedClientDict.pop(address)
            print(disconnected + "Adresli bağlantı disconnect oldu")
            self.send_simple_msg_to_client("231", address)
        except:
            self.send_simple_msg_to_client("500", address)

    def send_simple_msg_to_client(self, message, clientAdress):
        """Client'e mesaj gönderme"""
        if (self.ServerSocket == None):
            print("Server Socket Oluşturulmamış mesaj gönderilemedi")
            return
        try:
            self.ServerSocket.sendto(str.encode(message), clientAdress)
            print("Mesaj gönderildi..")
        except:
            print("Mesaj gönderimi sırasında herhangi bir hata oluşmuş olabilir.")

    def send_datapacket_msg_to_client(self, address, command="", seqNumber=0, data=""):
        """Datapacket sınıfından bir nesne oluşturur ve onu cliente yollar
        cevap beklemez"""
        new_data_packet = datapacket.DataPacket(command, seqNumber, data)
        pickled_data_packet = pickle.dumps(new_data_packet)

        self.ServerSocket.sendto(pickled_data_packet, address)

    def md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def close_server_and_abort_program(self):
        """soketi kapa while döngüsünden çık"""
        self.ServerSocket.shutdown()
        self.ServerSocket.close()

input_ip = input("Lütfen sunucunun oluşturulacağı ip adresini giriniz")
s = FTPServer(ip=input_ip)
