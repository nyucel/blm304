* Server.py ve Client.py dosyaları linux ortamında çalıştırılmalıdır.
* Server.py ve Client.py dosyaları yönetici hakları kullanılarak çalıştırılmalıdır.

# SERVER
* Server.py çalıştırıldığında UTC değişkeninin değeri varsayılan olarak üzerinde çalıştırıldığı işletim sisteminin utc değerini alır.
* Değişiklik yapmadan çalıştırıldığında istemci zamanı, sunucu zamanı ile aynı olacak şekilde ayarlanır.
* İstemci tarafına ayarlanmasını istediğiniz UTC değerini girmek için server.py dosyasındaki UTC değişkenine integer değer girilmelidir(UTC=-3).
* Serverin çalıştırıldığı işletim sistemi UTC+3 zaman diliminde ise UTC değişkenine 5 değeri girilmesi durumunda istemci zamanı, sunucu zamanından 2 saat ileride olacak şekilde ayarlanır.

# CLIENT
* Client.py çalıştırıldığında istenen ip adresine sunucu.py nin çalıştırıldığı cihazın local ip adresi girilmelidir.
* Ip adresi girildiğinde sunucudan,sunucunun zaman bilgisi alınır(milisaniye cinsinden).
* Yaşanan gecikme hesaplanarak sunucudan aldığımız zaman bilgisinin üzerine eklenir ve bu değere göre istemci.py dosyasının çalıştırıldığı işletim sisteminin saati ayarlanır.
