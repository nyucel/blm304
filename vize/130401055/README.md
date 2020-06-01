Python3 ile Çalışan UDP Üzerinden Dosya Transfer Programları

Kullanım (2 ayrı komut satırı penceresinde):
sudo python server.py
sudo python client.py "sunucu_adresi"


Çalışma şekli:
Paketler binary formatta alınıp gönderilir.
Buffer boyutu 4096 KB.
Dosya yolu server.py nin çalıştığı dizinle değiştirilmelidir.
UDP kullanıldığı için paket kaybını görebilmek adına alınan ve gönderilen paket sayıları anlık olarak gösterilmektedir.


1. Client dosyası:

Program aşağıdaki kütüphaneleri kullanır.
socket (soket oluşturmak için)
os (dizin bulmak ve dosya aramak için)
sys (sys.exit() ile çıkış yapabilmek için)

Try ve except UDP soketin oluşturulmasını kontrol eder.

Sunucunun komut listesi göndermesi üzerine bu aşamada komut girilmesi beklenir.

"ls" komutu girildiğinde sunucudan içerik listesi alınır ve yazdırılır.

"get" komutu girildiğinde sunucu tarafından komutun doğrulanması ve ACK beklenir.
Dosyanın bulunduğu bilgisi sunucudan beklenir.
Mesaj kısaysa bulunduğu anlaşılır ve belirtilen dosya açılır.
Paket sayısına bağlı olarak veri eklenir.

"put" komutu girildiğinde sunucu tarafından komutun doğrulanması ve ACK beklenir.
Dosya mevcutsa boyut kontrol edilir, 4096 byte lık paketlere ayrılır.
Verinin tamamı okunana kadar boyuta bağlı olarak paket gönderimi devam edecektir.

"exit" komutu girildiğinde soket kapatılacak ve programdan çıkılacaktır.
İstemci bununla ilgili sunucudan bir bildirim almayacaktır.

Tanım dışında bir komut girildiğinde uyarıyla karşılanacaktır.


2. Server dosyası:

Program aşağıdaki kütüphaneleri kullanır.
socket (soket oluşturmak için)
os (dizin bulmak ve dosya aramak için)
sys (sys.exit() ile çıkış yapabilmek için)

Try ve except UDP soketin oluşturulmasını kontrol eder.

İstemciden komut beklenir.

"ls" komutu girildiğinde dizine gidilir, bütün dosyaların adı eklenip yollanır.

"get" komutu girildiğinde istemciye ACK gönderilir, dosya paketler halinde gönderilir.

"put" komutu girildiğinde istemciye ACK gönderilir, dosya paketler halinde alınır.

"exit" komutu girildiğinde soket kapatılacak ve programdan çıkılacaktır.

Tanım dışında bir komut girildiğinde uyarıyla karşılanacaktır.
