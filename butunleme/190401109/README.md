
# rota.py programı nasıl çalışır ?

Rota programı, UDP Traceroute gibi belli bir TTL değeri ile hedef makinenin
ulaşılmaz bir portuna (33434 ve 33534 arasında olan bir port numarası)
bir dizi UDP paketi göndermektir.

Karşıya gönderilen paket bir ağ yönlendiricisine her ulaştığında,
yönlendirici paketin TTL değerinin birden büyük (TTL > 1) olup olmadığını kontrol eder.

Paketin TTL değeri birden büyük ise, değerini birden azaltır (yeni TTL= TTL-1)
ve paketi bir sonraki yönlendiriciye iletir.

Eğer yönlendiriciye gelen paket TTL değerin bire eşit (TTL=1) ise,
yönlendirici paketi atar ve kaynak makineye paket TTL'sinin aşıldığı için
hedef makineye ulaşılamadığını bildiren bir "TLL Time exceeded" yanıtı gönderir.

Rota programı, bu ICMP zaman aşılmış yanıtlarını (ICMP Time exceeded message)
kullanarak kaynak ve hedef makinelerinin arasındaki yönlendiricileri bulmaktadır.
Yani kaynak makineden hedef makineye ulaşmak için paket hangi yönlendiricilerden
geçtiğini bulmaktadır.


Örneğin, sudo ./rota.py 8.8.8.8 komutu çalıştırıldığında
