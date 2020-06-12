Medya Han 170401040
# NETWORK TIME SERVER AND CLIENT

- **networkTimeServer.py** çalıştırıldıktan sonra **networkTimeClient.py** çalıştırılır.
- Bağlantı sağlanır sağlanmaz istemci sunucunun UTC bilgisini almasini bekler. 
- Sunucuda kullanıcı UTC bilgisini +2 veya -3 vb. şeklinde girdikten sonra istemci çalışmasına devam eder.
- Sunucu, gerekli gecikme süresi ölçümlerinden sonra güncel zamanı istemciye gönderir.
- İstemci güncel zamanı sunucudan aldıktan sonra sunucu bütün portları kapatır.
- Hemen ardından istemci, Linux tabanlı işletim sistemine özel olarak sistem zamanını sunucudan aldığı güncel zaman ile günceller.

**NOT:** İstemci (networkTimeClient.py) yalnızca Linux tabanlı işletim sistemlerinde çalışabilecek şekilde tasarlanmıştır.
