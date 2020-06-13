SERVER

Programı terminalden sudo python3 Server.py komutuyla sunucu çalıştırılabilirsiniz.

Program başlatılınca Sunucunun IP Adresini girmeniz gerekmektedir.

UTC değeri bir değişkende tutulmaktadır.

Server gecikme süresini bir fonksiyon içerisinde hesaplar ve ekrana yazdırır.

Program 'UTC +3'e göre ayarlanmıştır.

Server saati milisaniye cinsinden Client'a iletir ve görevini tamamlar.

Server sonlandırıldığı zaman portlar kapatılır.

CLIENT

Programı terminalden sudo python3 Client.py komutuyla çalıştırılır.

Program başlatılınca Hedef Sunucunun IP Adresi girilmelidir.

Client öncelikle Server tarafından milisaniye cinsinden gönderilen saat bilgisini yakalar ve ekrana yazdırır.

Sonrasında gelen saat bilgisine göre sistem saatini günceller ve ekrana yazdırır.

Server sonlandırıldığı zaman portlar kapatılır.