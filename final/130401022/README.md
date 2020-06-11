#sunucu .py 
  dosyası içersinde 'UTC' adlı değişkene {-12, -11 ,-10 , ..., 0 , +1 , +2 , +3 , ... , +12 } kadar integer değer verebilirsiniz.
  Böylelikle UTC değişkeni sunucunun yanıt olarak hangi zaman dilimini döndüreceği değerdir. Eğer integer dışında başka değer verirseniz sunucu
  kodları çalışmaz. 'sunucu_UTC' değişkeni sunucu.py dosyasının çalıştığı bilgisayar üzerinde ki zaman dilimidir. Böylelikle UTC ve sunucu_UTC arasındaki
  fark hesaplanır. Ardından aradaki saat farkının hangi yöne doğru hesaplanması gerektiği bulunup istenen saat, hesaplanan zaman_farki
  ile beraber milisaniye olarak hesaplanır. Sonrasında cevap olarak milisaniye ve 'UTC' değişkenin değeri gönderilir.
  
#istemci .py 
  İstemci dosyası içindeki 'IP' ve 'TPC_PORT' değişkenlerine sunucunun ip 'si ve kullandığımız '142' port numarası yazılmalıdır. Eğer sunucu
  ip'si değişirse daha sonra tekrarnan 'IP' değeri değiştirilebilir. Bunu 'sunucu.py' dosyasından kontrol edebilirsiniz. Sunucudan gelen yanıtı alan
  istemci "sunucu kod, çalışma sırası, algoritma mantığı ve 1024 kb verinin socket tarafından gönderilmesi ortalama 2 saniye olarak geçikme süresini hesaplar".
  Sonrasında istemci gönderilen milisaniye değerini parçalayarak elde ettiği saat bilgisini bilgisayarın saat bilgisi olarak ayarlar.
  
