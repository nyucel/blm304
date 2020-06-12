Yiğitcan ÜSTEK - 160401030

Sunucu

root yetkisi ile çalıştırılmalıdır.

Programı çalıştırırken sudo python3 server.py "ip_adresi"  bu komut ile çalıştırılmalıdır ve "ip_adresi" yerine bağlanılmak istenilen ip adresi girilmelidir.

var_time = "UTC+0" değişkeni ile zaman dilimi değiştirilebilir. Değiştirmek için "+0" yerine istenilen saat değerini giriniz. Örnek olarak; var_time = "UTC-1"

Sunucu ve istemci arasındaki paket gecikmesini yaklaşık olarak hesaplayıp istemciye gönderir. Hesapladıktan sonra sistem saatini değiştirecek saati yollar.




İstemci

root yetkisi ile çalıştırılmalıdır.

Programı çalıştırırken sudo python3 client.py "ip_adresi"  bu komut ile çalıştırılmalıdır ve "ip_adresi" yerine bağlanılmak istenilen ip adresi girilmelidir.


Gerçeğe yakın saati hesaplamak için sunucudan 100 defa alınan saat bilgisinin ortalamasını hesaplatıp gerçeğe yakın bir değer elde eder. Bu sayede en son aldığı saat bilgisi ile bu gecikme değerini toplayıp hatayı minumuma indirir. 
Son olarak sistem saatini 
	'sudo date --set="'+time.ctime(saat)+'"'
komutu ile değiştirir. 