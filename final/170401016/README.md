# AĞ ZAMAN SUNUCUSU ve İSTEMCİSİ

İlk etapta server.py nin, bunun ardından client.py nin çalıştırılması gerekmektedir.

Sunucu ve istemci GNU/Linux dağıtımlarında kullanılmak üzere tasarlanmıştır. Pop!_OS 19.04 ile test edilmiştir.


## Sunucunun başlatılması

    sudo python3 server.py


Sunucu çalıştırıldığında kullanıcıdan saat dilimini girdi olarak bekler.

Örneğin girdi olarak "3" (tırnak işaretleri olmadan) girmeniz durumunda sunucu UTC+3,  
"-2" (tırnak işaretleri olmadan) girmeniz durumunda sunucu UTC-2 yi saat dilimi olarak ayar.




## İstemcinin başlatılması

    sudo python3 client.py

İstemci kullanıcıdan girdi olarak sunucunun IP adresini girmesini bekler.


İstemcinin komut havuzunda 2 adet komut bulunur. S ve Q.

Kullanıcı S komutunu girdiyse sunucudan saat bilgisini talep eder ve makinesinin saatini bu saat ile değiştirir.

Kullanıcı Q komutunu girdiyse sunucu ile istemci arasındaki bağlantı çift taraflı şekilde koparılır.

