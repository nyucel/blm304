# Veri Haberlesmesi

##Python3 ile Calisan TCP uzerinden NTP sunucu ve istemci programları

###Kullanim (2 ayri komut satiri penceresinde):
```bash
sudo python server.py
```
```bash
sudo python client.py "sunucu_adresi"
```


###Calısma Şekli:
Sunucu IP client.py icerisinden de ayarlanabilir.
Zaman dilimi server.py uzerinden ayarlanabilir.
Buffer boyutu 1024 KB.
Sunucu butun isteklere sistem saatine(timestamp olarak) zaman dilimini ekleyerek cevap verir. 
