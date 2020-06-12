# Veri Haberleşmesi

##Python3 ile Çalışan TCP ile Çalışan NTP Sunucu ve İstemci Programları

###Kullanım (2 ayrı komut satırı penceresinde):
```bash
sudo python server.py
```
```bash
sudo python client.py "sunucu_adresi"
```


###Çalışma Şekli:
Sunucu IP client.py içerisinden de ayarlanabilir.
Zaman dilimi server.py üzerinden ayarlanabilir.
Buffer boyutu 1024 KB.
Sunucu bütün isteklere sistem saatine(timestamp olarak) zaman dilimini ekleyerek cevap verir. 
