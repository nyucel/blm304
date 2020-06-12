Emin Sekmenoglu - 130401091

İki adet dosyadan oluşmaktadır.
* İstemci.py
* Sunucu.py

Test adımları için pdb kütüphanesi kullanılarak test edildi.
Her adımdaki güncellenen değişkenler pdb.set_trace() ile duraklatılarak kontrol edildi.

IP adresi localhost olarak ayarlandı, gerçek bir IP girmek için test_ip değişkeninin güncellenmesi yeterlidir.
Yazılım ip/port bilgisini ekrana yazdırıyor. Tarih, zaman ve UTC zaman dilimi bilgisini gönderiyor. Gecikme süresini de ekleme yapıyor.

Server bağlantısı kuruluduktan sonra, serverdan gelen zaman, tarih ve UTC zaman dilimi bilgilerini, gelen zaman ve tarihe göre hesaplayıp, cihazın tarih ve saatini degiştiriyor.