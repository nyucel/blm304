170401008 Arzu Tepe
Sunucu Windows ve Linux'ta çalışır.
İstemci ise sadece Linux'ta çalışır.

-Sunucu çalışmaya başladığında öncelikle kullanıcıya zamanı değiştirip değiştirmek istemediğini sorar.
-Kullanıcı zamanı değiştirmek istiyor ise istediğini zamanı yazabilir. (Örnek yazım UTC+2 zaman dilimini istiyorsa +2 yazması yeterlidir.)
-Kullanıcı zamanı değiştirmek istemiyor ise yerel zaman dilimi kullanılır.
-Gecikme süresi sunucu ve istemci arasındaki bir mesaj ile ölçülmüştür.
-Sunucu zamanı milisaniyeye çevirir ve gecikme süresini de ekleyerek istemciye gönderir.

-İstemci sunucuya başarılı bir şekilde bağlandıktan sonra gelen saat bilgisini alır.
-Milisaniye cinsinden gelen zamanı tarih ve saat olarak çevirip cihazın saatini değiştiriyor.
