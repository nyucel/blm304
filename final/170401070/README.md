## Server:

Sunucunun IP Adresi girilir. Client ile gerekli bağlantılar sağlandıktan sonra sunucunun saat bilgisi istemciye gönderilir. Sunucu ile istemci arasındaki gecikme hesaplandıktan sonra saat bilgisine eklenmiş gecikme güncel zaman bilgisini oluşturur.Güncellenmiş zaman cliente gönderilir. Soketler kapatılır.
utc değişkeni ile zaman dilimi server.py dosyasında değiştirilebilir.

## Client:

Sunucunun IP Adresi girilir. Server ile bağlantı kurulur.Sunucu tarafından gönderilen zamanları yakalar. Soketler kapatıldıktan sonra sistem saatini günceller.


Terminal ekranında önce sudo python3 server.py komutuyla NTP Server çalıştırılır.
Başka bir terminal ekranında sudo python3 client.py komutuyla NTP Client çalıştırılır.	






