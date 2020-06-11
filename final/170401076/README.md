* **sunucu.py** ve **istemci.py** dosyaları Linux ortamlarında çalıştırılmalıdır.
* Her iki dosyada yönetici haklarıyla çalıştırılmalıdır.
## Sunucu
* Sunucu bağlantıyı TCP üzerinden sağlayarak, 142. portu dinlemektedir.
* Sunucu bağlanan istemcilere zamanı milisaniye ve zaman bilgisini "UTC+3" şeklinde göndermektedir.
* Sunucu bağlanan istemcilerin zamanlarını ayarlarken üzerinde çalıştığı işletim sisteminin zaman bilgisini kullanır.
* **sunucu.py**'deki **UTC** değişkeni üzerinden zaman dilimi **"UTC+5"**, **"UTC-3"** şeklinde değiştirilebilir.
* Örnek olarak sunucunun işletim sisteminde zaman dilimi **"UTC+3"** ve sunucuda bulunan **UTC** değişkeni **"UTC+5"** olarak belirtilirse bağlanan istemcinin saati, sunucu saatinden 2 saat ileride olacak şekilde ayarlanacaktır.
## İstemci
* **istemci.py** çalıştırıldığında IP adresi olarak **sunucu.py**'nin çalıştırıldığı cihaza atanan local IP adresi girilmelidir.
* Daha sonra sunucudan gelen milisaniye ve zaman bilgisi kullanılarak, oluşan gecikmeleride hesaba katarak zaman bilgisini istenilen şekilde ayarlanır.
