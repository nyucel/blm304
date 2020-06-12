# Veri Haberleşmesi 

```
istemci.py ve sunucu.py dosyaları linux tabanlı işletim sistemine sahip bilgisayarlarda çalışmaktadır.
``` 

Bircan Arslan 170401013

## Sunucu

- Sunucuyu başlatmak için  `$ sudo python3 sunucu.py ` komutunu yazmalısınız.
- Sunucu, başlatıldığı bilgisayarın IP adresini otomatik olarak alıp, ekrana aldığı IP adresini yazacaktır.
- Sunucu 142. portu dinlemektedir.
- Utc değiştirmek istiyorsanız sunucu kodunun 11. satırında bulunan girilenutc değişkenini tam sayı olarak "UTC+03","UTC-03" formatında değiştirebilirsiniz. 
- Saati ayarlamak için enter tuşuna basmalısınız. Böylece saat değeri istemciye gecikme hesaplanarak gönderilir.
- Sunucu, kapatılana kadar gelen tüm isteklere cevap vermeye devam eder.

## İstemci

- İstemciyi başlatmak için `$ sudo python3 istemci.py ` komutunu yazmalısınız.
- Sunucunun ekranında yazdırılan IP adresini istemciye yazarak bağlantıyı kurabilirsiniz.
- Sunucu tarafından saat bilgisi geldiğinde saat ayarlanır ve "Saat değiştirme başarılı!" uyarısı yazdırılır.
- İşlem tamamlandıktan sonra istemciyi durdurabilirsiniz.
