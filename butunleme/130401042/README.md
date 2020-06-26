# Nasıl çalışır?

Öncelikle kodlar `sudo python3 rota.py makine adı` şeklinde çalıştırılır.

Yapılan traceroute işlemi nesne yapısı içinde tanımlanmıştır. UDP paketi oluşturulup ilgili makine adını taşıyan makine ip'sine gönderilir.
ÙDP paketinin proto özelliği `(proto= socket.IPPROTO_UDP)` şeklinde ayarlanmıştır.
Daha sonra İCMP paketi oluşturulup ilgili makine ip'sinden gelen mesajı bu paket ile alınır.
İCMP paketinin proto özelliği `(proto=socket.IPPROTO_ICMP)` şeklinde ayarlanmıştır. `Ttl` degeri 1 den başlatılıp her değer için bu işlemler while döngüsünde tekrar edilerek
geçilen her yönlendiricinin ip adresi kaydedilir. Daha sonrasında `rota.txt` text belgesi içine yazılır. Eğer yönlendirici UDP paketine cevap vermemiş ise yönlendirici
ip'si otomatik olarak `**` şeklinde ayarlanır. Aynı şekilde `rota.txt` text belgesi içine yazılır. Ttl değeri 30 ile sınırlandırılmış olup bu değer aşıldığında program sonlanır.
