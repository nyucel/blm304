# SUNUCU
Sunucu, Windows tabanlı bilgisayarlarda çalışmaktadır. Sunucuyu çalıştırmadan önce IP adresini manuel olarak girmemiz gerekir. İstemci ile sunucu arasındaki bağlantı kurulduktan sonra sunucuya zaman dilimini girmemiz gerekiyor (Örneğin, UTC + 3 için: +3 yazılmalı). Zaman dilimi girildikten sonra sunucu istemciye üzerinde koştuğu işletim sisteminin saatini gönderiyor.


# İSTEMCİ
İstemci Linux tabanlı bilgisayarlarda çalışmaktadır. Sunucu ile aynı şekilde IP adresi manuel olarak girilmelidir. Sunucu ile bağlantı kurulduktan ve sunucuya zaman dilimi girildikten sonra, sunucudan aldığı zaman bilgisine veri gönderip alırken yaşanan gecikme zamanını da ekleyerek bilgisayarın saatini değiştiriyor.