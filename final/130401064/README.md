
Programımız sunucu ve istemci olmak üzere iki ayrı programdan oluşmaktadır.
Sunucu uygulaması TCP time server yani zaman sunucudur. 142 nolu porttan hizmet vermektedir.
Sunucu uygulaması server.py dosyasındadır. İstemci uygulaması client.py dosyasındadır.
Sunucu tarafında ayrıca utc.txt isimli bir dosya bulunmaktadır. Bu dosya içine zaman dilimi bilgisi yazılmaktadır. Formatı UTC+2, UTC-2, UTC+0 şeklindedir.
Sunucu uygulaması bir istemci bağlantısı kabul ettiğinde bu bağlantı bir thread'e yönlendirilir.
İstemciden 'Time' şeklinde bir string veri gönderilir. Bu mesajı alan sunucu o anki sistemin zamanını milisaniye cinsinden UTC olarak alır, utc.txt dosyasından okuduğu zaman dilimi bilgisiyle beraber istemciye gönderir.
Gönderilen mesajın formatı: 'Time:<milisaniye cinsinden zaman>;UTC:<zaman dilimi>' şeklindedir.
İstemci tarafında veri gönderilmeden hemen önce ve veri alındıktan hem sonra sonra zaman bilgileri alınarak geçen zaman hesaplanır. Bu zaman RTT'dir. (Round trip time)
İstemci tarafı veriyi aldığında bu bilgisi ayrıştırarark parse eder ve milisaniye cinsinden zamanı ve zaman dilimini alır.
Milisaniye cinsinden zaman alınan zaman datetime fromatına çevrilir. Üzerine UTC eklenir (ya da çıkarılır). Son olarak sunucu tarafından istemciye gelene kadar geçen zaman bu zamana eklenir.
Bu zaman yaklaşık olarak RTT/2'dir. Hesaplanan zaman bilgisi Windows ortamında win32api.SetSystemTime fonksiyonu ile sistemin zamanı olarak atanır.

Not: Bu fonksiyon yetkilerin olmadığı zaman hata vermektedir. Bu yüzden hesaplanan zaman ayrıca ekrana baştırılmaktadır.
