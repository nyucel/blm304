Sunucu

* Sunucu root yetkisi ile çalıştırılmalıdır.

* Sunucu aynı anda birden fazla istemciyle bağlantı kurabilir ve zaman bilgisi gönderebilir.

* server.py dosyasındaki `TIMEZONE` değişkeni ile zaman dilimi ayarlanabilir.

* TIMEZONE değişkeni `"UTC"` `"UTC+3"` `"UTC-2"` gibi değerler alabilir.


İstemci

* İstemci başlatıldığında sunucuya bağlanmak için sunucunun adresi girilmelidir.

* Sunucuya bağlandıktan sonra saati ayarlamak için `ENTER` tuşuna basılmalıdır.

* Bağlantıyı sonlandırmak ve programdan çıkmak için herhangi bir tuşa basılmalıdır.
