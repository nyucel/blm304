	Server Windows ve Linux tabanlı bilgisayarlarda çalışmaktadır.ServerTCP.py dosyasını çalıştırmadan
IP adresini manuel yazmamız gerekiyor. Ip yazıp çalıştırdıktan sonra clientdan gelen IP ve PORT bilgisini
ekrana yazdırıyor. Daha sonra cliente tarih, zaman ve UTC bilgisini gönderiyor. Buradaki zamana yaklaşık
gecikme süresini hesaplayarak ekleme yapıyor ve zamanı öyle gönderiyor. Son olarak bağlantıyı kesip diğer
bağlantıları bekliyor.
	
	Client sadece Linux tabanlı bilgisayarlarda çalışmaktadır. Tıpkı Server gibi IP adresini manuel olarak 
girmemiz gerekiyor. Ip adresini girdikten sonra servera bağlanıyor ve "Hello, SERVER!" mesajını gönderiyor.
Daha sonnra serverdan gelen zaman, tarih ve UTC bilgilerini ekrana yazdırarak gelen zaman ve tarihe göre
cihazın tarih ve saatini degiştiriyor.
