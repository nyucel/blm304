# KULLANIM

- Eğer linux kullanıyorsanız terminalden sudo python3 `server.py` komutuyla sunucu çalıştırılabilirsiniz.
- Eğer Windows kullanıyorsanız 'komut istemi' yönetici olarak çalıştırmanız yeterlidir. 
- Önce `sunucu.py` daha sonra ``client.py` calıştırmanız gereklidir.
- ìstemci dosyası içindeki `os.system("sudo date --s  '%s'" % linux)` kodunun çalışması için gerekli ayarlamaları yapmış olmanız gereklidir.
- Linux terminalinden `sunucu.py` dosyasını `sudo` yetkisiyle açmanız yeterlidir.

- #### Sunucu :
  sunucu dosyası içersinde default olarak sunucu ip'si : `127.0.0.1` olarak girilmiştir.
  Yanıt olarak göndermek istediğiniz utc değerini sunucu dosyası içersindeki `UTC_ZAMAN_DILIMI` değişkeni ile değiştirebilirsiniz.Değişken sadece string türünden değerler girmelisiniz ve girdiğiniz değerler örneğin('UTC-2')
  gibi olmalıdır.
  
- #### İstemci :
  istemci dosyası çalıştığında sunucuya bağlanabilmek için sunucu ip'sini elle girmeniz gereklidir.
  istemci dosyası içersindeki `gecikme_suresi` adlı değişken gecikme süresini `baslangic` ve `bitis` değişkenlerini kullanarak hesaplar. Bu değişkenlerin çalışma mantığı ortasında olan `gelenCevap` adlı değişken gelene kadar ne kadar milisaniye geçmiştir?.
