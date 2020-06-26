


Programın root haklarıyla çalıştırılıp çalıştırılmadığı kontrol edilir. Sonra random bir porttan ttl'i 1 olan udp paket gönderilir ve cevap gelmesi beklenir. Beklenen cevap icmp türünden bir cevaptır.Gönderici ip adresi aradaki yönlendiricinin ip'si olmaktadır. Devamında ttl birer birer arttırılarak maksimum 30'a kadar bu işlemler devam edilir. Her ttl de gönderilen udp paketten cevap alınamazsa toplamda 3 kez tekrar gönderilir. Gelen icmp paketlerindeki gönderici ip adresleri txt dosyasına yazılmaktadır. Sonra tüm işlemler tamamlandıktan sonra  program sonlanmadan dosya ve socket kapatılmaktadır.


Programın kullanımı aşağıdaki gibidir.

-sudo python3 rota.py orneksite.com
  


  
  
