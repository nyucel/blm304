# Simple NTP SERVER-CLIENT
# 170401009 -Atakan Türkay
### Kullanım:
    -Sadece linux üzerinde ve sudo yetkisi ile çalışır.
##### SERVER
```sh
$ sudo python3 server.py
```
    -Kodu ile server başlatılır.
    -server scapy ile ağdaki lokal ip adresini öğrenir ve 127 nolu portu dinlemeye başlar.
    -Clientten gelen TCP 3 lü el sıkışma ile bağlantı başlar.
    -Clientten "TIME_REQUEST" isteği aldığı zaman t1 zamanını kaydeder
    -Cliente Timezone değerini , Zaman değerini(ms) ,t1 zamanını , ve serverden paketin çıktığı t2 zamanını yollar.
##### CLIENT
    -client_py = client_paket_yoneticisi("192.168.0.105", 127) satırındaki ip adresine server ip adresi girilir.
```sh
$ sudo python3 client.py
```
    -Kodu ile client başlatılır.
    -Client kendi üzerinden random bir port açarak Server ile 3lü el sıkışması gerçekleştirir.
    -Zaman yönetici nesnesi paket yöneticisi nesnesinden zaman isteği yapmasını söyler.
    -Zaman yöneticisi servere "TIME_REQUEST" isteği atar ve attığı zamanı t0 değeri içerisine kaydeder
    -Serverden zaman bilgileri geldiği zaman zaman yöneticisi t1 değerini kaydeder.Ve gelen cevapla birlikte bu zaman değerlerini zaman yöneticisine yollar.
    -Zaman yöneticisi bilgileri ayrıştırır ve içerisinden gelen zamanı saniye cinsine çevirir.
    -Zaman yöneticisi gecikmeyi hesaplar
    gecikme = (self.t3-self.t0) - (self.t2-self.t1)
    -Gecikmeyi ve gelen zaman bilgisini ekleyip linux sistemde "sudo date -s [ZAMAN]" komudunu çalıştırır ve zamanı ayarlar.
    -Zaman senkronizasyonu hakkında yaptığım araştırmada , gelen paketlerin zamanları ,offsetleri istatiksel olarak birkaç paket dizisi yollanıp hesaplanarak en doğru zamanın seçildiği bilgisi yazıyordu.Ben üstteki verdiğim formülle hesapladım.Sezyum saat dışındaki saatlerin belli bir zaman sonra geriden geldiğini okudum.Bunun için offset değeri hesaplanıyor diye anladım.
[![NTP-DELAY](https://upload.wikimedia.org/wikipedia/commons/8/8d/NTP-Algorithm.svg)](https://en.wikipedia.org/wiki/Network_Time_Protocol)