Kullanım Şekli

Traceroute benzeri bir şekilde istek yapmak istenilen hedef makinenin adını : sudo python3 rota.py hedefmakineadı şeklinde girilir. Örnek olarak sudo python3 rota.py www.comu.edu.tr . 

<img width="510" alt="Ekran Resmi 2020-06-24 16 51 16" src="https://user-images.githubusercontent.com/33404285/85569485-4084eb80-b63b-11ea-96cf-4ca68be02b70.png">

Kodun çıktısı, geçilen yönlendiricilerin IP adreslerinin rota.txt dosyasına yazdırılmasıdır.

Kodun Çalışması

Alıcı ve gönderici soketler oluşturmak için icmp ve udp nesneleri oluşturuldu. Icmp soketi gelen paketleri almak için, Udp soketi ise göndermek için oluşturuldu. Argüman ile verdiğimiz hedef makineye ulaşana kadar hangi yönlendiricilerden geçildiğini TTL değeri 1 arttırılarak bulunur. Yönlendiriciye deneme yapılırken kullanmak için bir zaman aşımı değişkeni tanımlandı. Sunucu zaman aşımına uğrar ise toplam 3 kere olmak üzere deneme yapılmaya ve adres alınmaya çalışılır. Bulunan yönlendirici IP adresi dosyaya yazılır ve TTL değeri değiştirilerek bir sonraki yönlendiriciye geçilir. Hedef makine adresine ulaşıldığında ya da TTL değeri 30 a ulaştığında program sonlanır.
