 Teminalden "sudo python3 sunucu.py" komutu ile sunucu yazılımı çalıştırılır.  
 Program başlatılınca zaman dilimi girilir(+3,-2 gibi).
 Ardından sunucu IP adresi girilir.
 
 Teminalden "sudo python3 istemci.py" komutu ile istemci yazılımı çalıştırılır. 
 Program başlatılınca hedef sunucunun IP adresi girilir. 

 Sunucu önce zaman dilimini sonra da o anki zamanı milisaniye cinsinden istemciye gönderir.
 İstemci yazılımında, ilk mesaj alındıktan sonra ve ikinci mesaj alındıktan sonra istemci
kendi saatine göre farkı hesaplar(milisaniye cinsinden).
 İstemci sunucunun gönderdiği milisaniye cinsinden zamanı, zaman dilimini
ve kendi hesapladığı gecikmeyi epoch'a ekleyerek sistemin saatini ayarlayacağı zamanı hesaplar.