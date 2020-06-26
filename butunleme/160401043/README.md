

# rota.py Nasıl Kullanılır?

- Programın çalıştırılması için sudo python3 rota.py hedefmakine komutunun girilmesi gerekmektedir.
- ÖRNEK: sudo python3 rota.py www.comu.edu.tr 


# Program Nasıl Çalışmaktadır?

- Program çalıştırıldığında öncelikle parametre olarak hedef bir makine girilip girilmediğini kontrol etmektedir.
- Hedef makineye ulaşılana kadar geçtiğimiz yönlendiricileri bulmak için TTL değeri her seferinde 1 arttırılmaktadır.
- Zaman aşımı hatasının önüne geçmek için gönderilen UDP paketine cevap gelmemesi durumunda, paketin gönderme işlemi en fazla 3 kez tekrar denenmektedir.
- Program en fazla 30 yönlendiriciye kadar deneme yapmaktadır.
- Son olarak ise programın çıktıları rota.txt dosyasının içerisinde yazdırılmaktadır.



