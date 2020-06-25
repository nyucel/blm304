##### Veri Haberleşmesi Bütünleme Ödevi #####

- Kütüphane olarak scapy kulanıldı.

- Kod asagida ki sekilde terminal üzerinden calistirilir.

```
 python3 rota.py makineAdi

```

- En fazla 30 yönlendiriciye kadar deneme yapılıyor

- Terminal üzerinde makine adını aldıktan sonra hedef makine için IP VE UDP paketleri gönderiliyor.

- Her paket 3 kez gönderilir.

- Hedef bilgisayara gonderilen UDP paketleri default olarak 33434 hedef porta gönderilir.

- Kapalı olan hedef port geriye "ICMP Destination Port Unreachable" mesajını gönderir. Geri dönen yanıt Type 3'dür.

- Hedef adres yanıt göndermezse ttl değeri tekrar arttırılıp devam eder.

- Belirlenen yönlendirici adresleri dizin içerisinde oluşturulan rota.txt dosyasına kayıt edilir.

