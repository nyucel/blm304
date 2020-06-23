
# rota.py programı nasıl çalışır ?

Rota programı, UDP Traceroute gibi belli bir TTL değeri ile hedef makinenin
ulaşılmaz bir portuna (33434 ve 33534 arasında olan bir port numarası)
bir dizi UDP paketi göndermektir.

Karşıya gönderilen paket bir ağ yönlendiricisine her ulaştığında,
yönlendirici paketin TTL değerinin birden büyük (TTL > 1) olup olmadığını kontrol eder.

Paketin TTL değeri birden büyük ise, değerini bir azaltır (yeni TTL= TTL-1)
ve paketi bir sonraki yönlendiriciye iletir.

Eğer yönlendiriciye gelen paket TTL değerin bire eşit (TTL=1) ise,
yönlendirici paketi atar ve kaynak makineye paket TTL'sinin aşıldığı için
hedef makineye ulaşılamadığını bildiren bir "TLL Time exceeded" yanıtı gönderir.

Birinci adımda, ilk paket hedef makineye göndermeden önce paketin TTL değeri 1 (TTL = 1) sayısına eşittir.
Paket gönderip, yanıt geldiğinde gelen ICMP paket kaynak ip adresi okunmaktadır.
Sonraki gönderilecek paketler de benzer şekilde TTL değerlerin bir (TTL=TTL+1) artırılır **maksimum hops**(yönlendirici) sayısına kadar.
Varysayılan olarak HOPS_MAX = 30.

Böylece, Rota programı bu ICMP zaman aşılmış yanıtlarını (ICMP Time exceeded message)
kullanarak kaynak ve hedef makinelerinin arasındaki yönlendiricileri bulmaktadır.
Yani kaynak makineden hedef makineye ulaşmak için paket hangi yönlendiricilerden
geçtiğini bulmaktadır.

# Ancak  program paket hedef makineye ulaştığını nasıl anlayacak?

Rota programı bunun hakkında bilgi sahibi olacaktır, çünkü paketin orijinal alıcısı (hedef makine) talebi aldığında gelen ICMP yanıtı "**TTL Time exceeded**" mesajından tamamen farklı bir ICMP mesajı (**ICMP Destination/PORT Unreachable**) gönderecektir. Ayrıca cevap olarak gelen ICMP paketin kaynak ip adresi hedef makinenin ip adresi ile eşit olamlıdır.

# Program nasıl kullanılır?

Aşağdaki gibi kullanılmaktadır.

### sudo ./rota.py google.com 

veya

### sudo ./rota.py 8.8.8.8

Program hem rota.txt doasyasina çıktısını yazar hem de stdout (ekrana) yazmaktadır.
