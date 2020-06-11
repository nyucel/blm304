### İşletim sistemi
 - Sunucu ve client dosyaları hem Windows'ta hem Linux'ta kullanılabilir.
 - Client dosyasının saat değiştirme fonksiyonu yalnızca Linux cihazlar için ayarlanmıştır.
### Sunucu
 - Sunucu bilgisayarın IP adresinde ve 142.portta socket açarak çalışıyor.
 - Eğer port kullanımdaysa çalışmıyor.
 - Başlatıldıktan sonra gelen tüm isteklere saati yollayarak sonsuz döngüde çalışıyor
### Client
 - Başlangıçta sunucu IP adresi giriliyor.
 - Eğer sunucu bağlantısı başarılıysa zaman bilgisini sunucudan alıyor.
 - Gecikme değerini ekleyip sistem saatini ayarlıyor.
 Not: SuperUser izinleri verilmezse saat değiştirilemiyor
### Zaman dilimi değiştirmek
 - Zaman dilimi değiştirmek için server.py dosyası içerisindeki TIMEZONE değişkeni değiştirilmeli.
 ```
 TIMEZONE="UTC+0"
 ```
 - Yalnızca UTC zaman dilimi kabul ediyor.
 - UTC yazdıktan sonra +7 , -3 , -2 gibi ekleme yapılmalı.