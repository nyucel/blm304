Sunucu

Sunucuyu başlatmak kullanmanız gereken komut:
sudo python3 server.py

Sunucu, UTC +00 olarak başlar ve başlamadan önce size bu değeri değiştirmek isteyip istemediğinizi sorar.
Eğer UTC değerini değiştirmek isterseniz, sizden yazım kuralı olarak +03 veya -03 gibi bir değer beklenmektedir.

Sunucuya, bir istemci bağlantı kurduğu an varsayılan olarak tarih bilgisini gönderir.


İstemci
İstemciyi başlatmak kullanmanız gereken komut:
python3 client.py

İstemci, sunucuyla bağlantı kurduğunda sunucu makinenin tarih bilgisini mesaj olarak alır ve çıktı gösterir.
Eğer daha sonra yine tarih anlık tarih bilgisi alınmak istenirse GET komutu girilir ya da istemci makineye, sunucu makineden gelen tarih ayarlanmak isterse SET komutu girilir. Çıkış yapmak için Q komutu yazılır
