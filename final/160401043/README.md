

# SERVER

- Server'ı çalıştırmak için 'sudo python3 server.py' komutunu çalıştırmanız gerekmektedir.
- Program başlatılınca Sunucunun IP Adresini girmeniz gerekmektedir.
- Program 'UTC +3'e göre otomatik ayarlanmıştır. Dilerseniz kodun içerisinden bu kısmı düzeltebilirsiniz.
- Server gecikme süresini bir fonksiyon içerisinde hesaplar ve ekrana bastırmaktadır.
- Server son olarak saati milisaniye cinsinden Client'a iletir ve görevini tamamlar.
- Server sonlandırıldığı zaman portlar kapatılır.


# CLIENT

- Client'i çalıştırmak için 'sudo python3 client.py' komutunu çalıştırmanız gerekmektedir.
- Program başlatılınca Hedef Sunucunun IP Adresini girmeniz gerekmektedir.
- Client öncelikle Server tarafından milisaniye cinsinden gönderilen saat bilgisi yakalar ve ekrana bastırır.
- Client sonrasında gelen saat bilgisine göre sistem saatini günceller ve ekrana bastırır.
- Client sonlandırılırken tüm portlar kapatılır.

