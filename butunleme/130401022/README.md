## Nasıl çalışır ?

  Kullanıcının girdiği makina adına paket göndermek için `UDP` paketi oluşturur.
Ardından gelen cevabı almak için `İCMP` paketi oluşturur. `mesaj , adres = aliciPaket.recvfrom(BUFFER_SIZE)` kodu ile `İCMP` paketine gelen mesajın adresini kaydeder.
Bu adres ilgili time to live(ttl) değerine karşılık gelen yönlendirici adresidir. Daha sonra ilgili ttl numarasını ve yönlendirici adresini `rota.txt` adlı metin
belgesine yazar.

## Nasıl kullanılır ?

  Örnek kullanım olarak ubuntu işletim sisteminde :   `sudo python3 rota.py makinaAdi` şeklinde çalıştırılır. Makina adının eksik yada yanlış girilmesi durumunda kod çalışmayıp kendi kendini imha edecektir. Bu durumda doğru makina adı ile tekrar deneyiniz.
