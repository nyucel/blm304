- server.py ve client.py yazýlýmlarý linux ortamýnda çalýþmaktadýr.
- server.py dosyasý çalýþtýrmak için 'sudo python3 server.py' komutu girilmelidir.
- client.py dosyasý çalýþtýrmak için 'python3 client.py' komutu girilmelidir.

SUNUCU:
- sunucu 142. portu dinlemektedir.
- sunucu zamaný dilimini UTC-3 biçiminde, milisaniye cinsinden döndürmektedir.
- server.py dosyasýnýn 7. satýrýnda bulunan utc_time deðiþkeni ile istemcinin döndüreceði UTC zaman dilimi ayarlanabilir.

ÝSTEMCÝ:
- istemci hedef portu 142'dir.
- client.py dosyasý çalýþtýrýldýðýnda sunucu ip adresi girilmelidir.
- istemci ntp senkronizasyonunu kapatarak sunucudan aldýðý yanýta göre zaman dilimini ayarlar.