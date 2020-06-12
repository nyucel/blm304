
# NTP SERVER ve NTP CLIENT

- **Beyza ÇOBAN-170401012**

Öncelikle sudo python3 server.py komutu kullanılarak sunucu çalıştırılır.
Kullanıcıdan bağlanılacak olan IP bilgisi alınır.
UTC bilgisi değişkende tutulur. İsteğe göre güncellenebilir. (-2 veya +3 vb.) 
UTC bilgisi dosyaya yazılır.

Sunucudan Ip bilgisi alındıktan sonra sudo python3 client.py komutu kullanılarak istemci çalıştırılır.
Bağlanılacak olan Ip bilgisi kullanıcıdan alınır.
Kullanılan zaman dilimi yazıldığı dosya içerisinden okunup kullanıcıya döndürülür.
İstemci-Sunucu bağlantısı gerçekleştirilir.

Sunucu, gecikme süresini bulmak için istemciye kontrol amaçlı o anki zamanı gönderir ve karşılığında bir mesaj alır.
Gönderim ve alım zamanı kullanılarak sunucu tarafından gecikme süresi hesaplanır.
Gecikme süresi eklenmiş zaman istemciye gönderilir.

İstemci, yeni zamanı sunucudan aldıktan sonra sunucu bütün portları kapatır.
İstemci, sunucudan aldığı yeni zamana göre Linux tabanlı işletim sisteminde sistem zamanını yeni zaman ile değiştirir.



