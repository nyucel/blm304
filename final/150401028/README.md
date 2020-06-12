# Veri Haberleşmesi Final 
Bartu Utku SARP - 150401028
### Kullanım 

#### Sunucu

* Sunucuyu başlatmak için aşağıda yazılan komutu girmelisiniz.
```$ sudo python3 server.py ```
* Sunucu, bulunduğu bilgisayarın IP adresini `otomatik` olarak alır ve bu adresi istemciye girebilmeniz için ekrana yazdırır.
* Utc değiştirmek istediğinizde kodda bulunan utcdegeri isimli değişkene `UTC+03, UTC-03, UTC+1030` formatında bir UTC değeri yazarak değiştirebilirsiniz.
* Sunucu önce bulunduğu makinanın tarihini, saatini (milisaniye dahil) ve UTC'sini ekrana yazdırır. 
* Sunucu istemciye bağlandığında saati otomatik olarak değiştirilecektir. Bu sırada sizden superuser şifreniz istenebilir.
* Ayarlamak istediğiniz saat gecikmeler de hesaba katılarak istemciye gönderilir.
* Sunucu başlatıldıktan sonra sunucu kapatılana kadar tüm isteklere cevap vermektedir.

#### İstemci

* İstemciyi başlatmak için aşağıda yazılan komutu girmelisiniz.
```$ sudo python3 client.py ```
* Sunucu ekranında yer alan IP adresini girerek bağlantıyı başlatabilirsiniz.
* Sunucu tarafından ayarlanmak istenen saat bilgisi geldiğinde saat değişir ve ekranda `Saat değiştirildi` mesajı görüntülenir.
* Ardından istemci bağlantısı sonlandırılır.

### Hatırlatma

```Server.py dosyası Linux ve Windows tabanlı işletim sistemine sahip bilgisayarlarda, client.py dosyası ise Linux tabanlı işletim sistemlerinde çalışmaktadır. ```

```Sunucu 142. Portu dinlemektedir. ```