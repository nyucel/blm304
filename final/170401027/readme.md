Server

Server'i 'sudo python3 server.py' komutu ile calistirabiliriz.

Sunucu ip adresini 'server.py' dosyasi icindeki 'server_address' uzerinden degistirebiliriz.

Server dosyasindeki 'tz' degiskeni default olarak "UTC+3" olarak ayarlanmistir.

Client'dan "ok" mesaji geldiginde server.py anlik olarak fonksiyonu calistirir ve saati client'a gonderir.

Gonderim tamamlandiktan sonra server.py herhangi bir 'ok' mesajini beklemeye devam eder.


Client

Client'i 'sudo python3 client.py' ile calistirabiliriz.

Hedef sunucunun ip adresini 'server_address' degiskeni icinde degistirebiliriz.

Client 'ok' mesajini gonderdikten sonra kendi sistem saatine ait saniye ve milisaniyeyi alir.

Server'dan cevap geldikten sonra tekrar ayni islemi uygular ve aradaki milisaniye farkını cevap olarak gelen zamana ekleyerek kendi sistem saatini degistirir.

Ayarlanan saati bastiktan sonra baglanti sonlandirilir.