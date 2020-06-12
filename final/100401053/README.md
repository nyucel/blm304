##### client.py #####

- Kullanıcıdan ip adresi ve port bilgisi input olarak girmesi beklenmektedir.

- Server'a mesaj göndermeden önce sistem saatini SendMessageTime degişkenine atar.

- Bu mesaj geldiği zamanı da alıp server gönderiminde oluşan zaman gecikmesini timeSpent değişkenine atar ve bu süreyi hesaba katarak hesaplama yapar.

- Server'dan gelen mesaj milisaniye ve zaman dilimi şeklindedir.

- Server'dan gelen mesaj time_tuple değişkenine atanır daha sonra setComputerTime metodu ile bilgisayarın saatini ayarlar.


##### server.py #####

- Server zaman bilgisi olarak kendi işletim sistemi saatini almaktadir.
 
- Zaman bilgisi timeZone degiskeni ile değiştirilebilir.

- Zaman bilgisi sistem saatinin bulunduğu zaman diliminde farkli ise ona göre hesaplama yapip cevap gönderir.

- Server cevap olarak sistem saatini milisaniye cinsinden ve timeZone bilgisini gonderir gonderir.