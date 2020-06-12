


###  SERVER
  

 - Programı terminalden sudo python3 Server.py komutuyla sunucu
   çalıştırılabilirsiniz.
   
 
 - Program başlatılınca Sunucunun IP Adresini girmeniz gerekmektedir.

   
  - UTC değeri bir değişkende tutulmaktadır.
   
  - Program 'UTC +3'e göre otomatik ayarlanmıştır. Dilerseniz kodun
   içerisinden bu kısmı değiştirebilirsiniz.
   
   - Server gecikme süresini bir fonksiyon içerisinde hesaplar ve ekrana
   yazdırmaktadır.
   
  - Server son olarak saati milisaniye cinsinden Client'a iletir ve
   görevini tamamlar.
   
  - Server sonlandırıldığı zaman portlar kapatılır.

  
  

###  CLIENT

  

- Programı terminalden sudo python3 Client.py komutuyla sunucu çalıştırılabilirsiniz.

- Program başlatılınca Hedef Sunucunun IP Adresini girmeniz gerekmektedir.

- Client öncelikle Server tarafından milisaniye cinsinden gönderilen saat bilgisi yakalar ve ekrana yazdırır.

- Client sonrasında gelen saat bilgisine göre sistem saatini günceller ve ekrana yazdırır.

- Server sonlandırıldığı zaman portlar kapatılır.