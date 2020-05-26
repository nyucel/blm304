class DataPacket:
    """ UDP başlığının veri kısmını bu classın bir nesnesi şeklinde yollayacağım.
    COMMAND = > MESAJIN AMACI
    SEQNUMBER = > DOSYAYI İLETİLECEKSE ARKA ARKAYA GELMESİ GEREKEN PAKETLERİ SIRALAYACAĞIM NUMARA
    DATA = > YOLLANAN İŞLENECEK OLAN VERİ
    CHECKSUM => VERİ TAM İLETİLMİŞ Mİ DİYE BUNUNLA KONTROL EDECEĞİM
    """
    
    def __init__(self,command,seqNumber,data):
        self.command = command
        self.seqNumber = seqNumber
        self.data = data
        self.checksum = 0 ## checksum değeri örnek oluşturulduğu an hesaplanıyor..(hesaplanmadı)
        
    def printDataPacket(self):
        text = 'VERI KOMUTU (NE ICIN KULLANILACAK) :  {}  \n SIRA NUMARASI : {} \n CHECKSUM DEGERI :  {} '.format(self.command,self.seqNumber,self.checksum)
        print(text)
        
       
        """Aşşağıdaki iki fonksiyon chechksum değerini hesaplamak için kullanılıyor, paketin oluşturulduğu
        yerdeki hesaplanan checksum değeri ile ulaştıktan sonraki değerin eşit olup olmadığı kontrol edilecek
        alltaki iki fonksiyonu şuradan aldım : 
        https://stackoverflow.com/questions/1767910/checksum-udp-calculation-python/1769267#1769267
        """
    
        
    def carry_around_add(self,a, b):
        c = a + b
        return (c & 0xffff) + (c >> 16)

    def calculateChecksum(self,msg):
        #s = 0
        #for i in range(0, len(msg), 2):
          #  w = ord(msg[i]) + (ord(msg[i+1]) << 8)
         #   s = self.carry_around_add(s, w)
        #return ~s & 0xffff
        return 0