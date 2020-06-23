
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

## Örnek

#### sudo ./rota.py facebook.com

Çıktısı:

route packets trace to facebook.com (69.171.250.35), 30 hops max, 28 byte packets

TTL = 1   onyxgateway.intranet (192.168.1.1) rtt = 0.0016 ms

TTL = 2   195.87.128.9 (195.87.128.9) rtt = 0.0170 ms

TTL = 3   31.155.48.213 (31.155.48.213) rtt = 0.0182 ms

TTL = 4   ae3-17-ucr1.ese.cw.net (195.2.23.153) rtt = 0.0174 ms

TTL = 5   ae1-ucr1.bch.cw.net (195.2.8.61) rtt = 0.0271 ms

TTL = 6   ae1-xcr1.bcp.cw.net (195.2.27.201) rtt = 0.0281 ms

TTL = 7   ae3.pr04.otp1.tfbnw.net (157.240.71.156) rtt = 0.0552 ms

TTL = 8   po106.psw02.otp1.tfbnw.net (157.240.51.187) rtt = 0.0286 ms

TTL = 9   173.252.67.65 (173.252.67.65) rtt = 0.0287 ms

TTL = 10  edge-star-mini-shv-01-any2.facebook.com (69.171.250.35) rtt = 0.0289 ms


Done, rota.py output >> rota.txt

