class DataPacket:
    """Bu sınıfta client ile server arasında gidip gelecek veriyi bir standarta oturtmak için yazdığım sınıf
    COMMAND = > MESAJIN TİPİ 
    SEQNUMBER = > DOSYAYI İLETİLECEKSE ARKA ARKAYA GELMESİ GEREKEN PAKETLERİ SIRALAYACAĞIM NUMARA
    DATA = > YOLLANAN İŞLENECEK OLAN VERİ
    CHECKSUM => VERİ TAM İLETİLMİŞ Mİ DİYE BUNUNLA KONTROL EDECEĞİM
    """
    
    def __init__(self,command,seqNumber,data,checksum):
        self.command = command
        self.seqNumber = seqNumber
        self.data = data
        self.checksum = checksum
        
    def printDataPacket(self):
        text = 'VERI KOMUTU (NE ICIN KULLANILACAK) :  {}  \n SIRA NUMARASI : {} \n CHECKSUM DEGERI :  {} '.format(self.command,self.seqNumber,self.checksum)
        print(text)
        
