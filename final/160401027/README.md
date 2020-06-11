160401027 - Göksu Türker
# Yapılandırma
## Sunucu
----
`server.py` dosyasında yapılandırma yapılacak kısım 14. satır ve 25. satır arasında.

### IP yapılandırma

Sunucunun IP'sini ayarlamak için 23\. satırda bulunan `IP` değişkenini değiştirerek ayarlayabilirsiniz.

`IP = "192.168.x.x"`

### UTC zaman dilimi yapılandırma

Eğer sunucu **yazılımının** zaman diliminde **sistemin** zaman dilimi değil de özel bir zaman dilimi kullanmak istiyorsanız, 
20\. satırda bulunan `UTC_OFFSET` değişkenine tam sayı(-7, 3, ex..) değeri vererek değiştirebilirsiniz.

Örnek:
`UTC_OFFSET = -4` veya `UTC_OFFSET = 3` gibi.

Eğer sunucu **yazılımının** zaman diliminde **sistemin** zaman dilimini kullanmak istiyorsanız,
20\. satırda bulunan `UTC_OFFSET` değişkenine `get_current_system_utc_offset()` fonksiyonunu atayabilirsiniz. 

Örnek:
`UTC_OFFSET = get_current_system_utc_offset()`

Sunucu yazılımı default olarak sistemin kullandığı zaman dilimini kullanır.

## İstemci
----
`client.py` dosyasında yapılandırma yapılacak kısım 7. satır ve 12. satır arasında.

### IP yapılandırma

İstemcinin bağlanacağı IP'yi ayarlamak için 10. satırda bulunan `IP` değişkenini değiştirerek ayarlayabilirsiniz.

`IP = "192.168.x.x"`

# Kullanım
## Sunucu
----
Terminalden `sudo python3 server.py` komutuyla sunucu çalıştıralabilir.

## İstemci
Terminalden `sudo python3 client.py` komutuyla istemci çalıştıralabilir.