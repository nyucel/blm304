class DataPacket:
    """ UDP başlığının veri kısmını bu classın bir nesnesi şeklinde yollayacağım.
    COMMAND = > MESAJIN AMACI
    SEQNUMBER = > ARKA ARKAYA GELMESİ GEREKEN PAKETLERİ SIRALAYACAĞIM NUMARA
    DATA = > YOLLANAN İŞLENECEK OLAN VERİ
    """
    
    def __init__(self,command,seqNumber,data):
        self.command = command
        self.seqNumber = seqNumber
        self.data = data
        
    def printDataPacket(self):
        text = 'VERI KOMUTU (NE ICIN KULLANILACAK) :  {}  \n SIRA NUMARASI : {}'.format(self.command,self.seqNumber)
        print(text)
        
