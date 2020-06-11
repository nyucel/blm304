- Server windows ve linux ortamında client sadece linux ortamında çalışmaktadır.
# Server
- Server 142. portu dinlemektedir.
- server.py dosyasının içindeki UTC isimli değişken değiştirilerek zaman dilimi değiştirilebilir.
```UTC="UTC+3" ``` değişken UTC-5 , UTC+2 şeklinde değiştirilmelidir.
# Client
  - Client açıldığında server ip adresinin girilmesi beklenmektedir.
  - Server ile bağlantı sağlandığında server saati milisaniye cinsinden ekrana yazdırılıp gecikme hesaplandıktan sonra clientin çalıştığı sistemin saati değiştirilir. 

