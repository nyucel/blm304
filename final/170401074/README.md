Batuhan ÖZALP - 170401074
Server saatinin doğru olduğu kabul edilerek işlemlere devam edilmelidir. 
Başlangıçta degisecek zaman dilimi, UTC 0'daki zaman, bilgisayarın zamanı ve bilgisayarın UTC değeri server ekranına yazdırılır.
Client ekranına serverdan gelen milisaniye cinsinden değer, serverın UTC değeri, degisecek zaman dilimi ve ayarlanması gereken zaman ekrana yazdırılır. Gecikme hesaplanır fakat client ekranında görünmez ve otomatik olarak zamana eklenir.

server.py dosyasında 6. satırda yer alan zaman_dilimi değişkeni ile değişmesi istenen zaman dilimi değiştirilebilir. +12 ve -12 arasında değer girilmelidir. Hata kontrolü yapılmamıştır.
Anlayamadığım şekilde server.py dosyası çalıştırıldığında s.bind("",142) komutunda hata verebilmektedir.
#setsebool -P httpd_can_network_connect 1  komutu çalıştırıldığında çözülebiliyor.

Her iki dosya da sudo ile çalıştırılmalıdır. sudo python3 server.py-client.py

İlk server çalıştırılır ve client bağlandığı anda serverin zamanı milisaniye olarak zaman ve zaman dilimi client yollanır. Aynı anda server dosyasına girilen zaman dilimi alınır ve saat değişikliği gerçekleştirilir.


