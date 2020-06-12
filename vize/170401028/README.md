# UDP kullanan FTP sunucu ve istemci

## Table of Contents

- [Hakkında](#about)
- [Yararlı bağlantılar](#links)
- [Çözülmeyi bekleyenler,eksiklik ve hatalar](#problemler)

## Hakkında <a name = "about"></a>

Ödevi hazırlayan : Emir Kıvrak 170401028

veri transferini UDP protokolü ile gerçekleştiren basit bir FTP sunucu ve istemcisi.

İleride kodu geliştirmek istediğimden baktığımda tekrar anlayabileceğim şekilde yazmak istedim bu yüzden class yapılarını kullandım, bundan dolayı kod biraz fazla uzadı.

Python 3 ile yazıldı, herhangi bir paket bağımlılığı yok

Necdet Yücel (@nyucel) hocamızın Veri haberleşmesi dersi vize ödevi için verdiği ödevin işlenmesidir.

## Yararlı bağlantılar <a name = "links"></a>

### ftp komutları ve dönüş değerleri
https://en.wikipedia.org/wiki/List_of_FTP_commands 
https://en.wikipedia.org/wiki/List_of_FTP_server_return_codes

### Başlamadan önce faydalandıklarım 

https://pythontic.com/modules/socket/udp-client-server-example  UDP server client örneği

https://realpython.com/python-sockets/ pythonda socket programlama 

https://dzone.com/articles/tcpdump-learning-how-read-udp tcpdump ile udp paketlerini okurken



## Çözülmeyi bekleyenler,eksiklik ve hatalar <a name = "problemler"></a>

- Bir UDP paketi maksimim 65,535 byte taşıyabiliyor , bu yüzden server bufferini bu değer seçtim,
yollanan dosyayı da 60 000 byte CHUNKSIZE olarak parçalıyorum. böylece dosya hızlı yollanıyor, fakat ya karşı taraf
bu kadar veriyi yazmaya yetişemeden bir sonraki paket yollanırsa? bunu şimdilik arka arkaya yollanan paketler
arasını biraz bekleterek çözdüm ? 

- Server asenkron çalışmadığından şu anda sadece bir client ile ilgilenebilir? yani sunucu dosya yollarken başka bir clientten istek gelirse?, server threadlara bölünebilir.

- Serverde ve clientteki dosyaları listeleme işlemi ayrı ayrı bir kaç kez yapılırsa bir sonraki işlemde çöküyor? bir daha başlattıktan sonra istenen işlem yapılabiliyor?
