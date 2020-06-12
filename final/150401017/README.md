SERVER

Server, yönetici yetkisi ve python3 ile veya windowsta çalıştırılmalır.
ip('127.0.0.1), port(142) ve zaman dilimi(UTC+3) kodun içerisinde yer almaktadır.
UTC+3 e göre saat ayarlanır değiştirmek istenirse kodun icerisindeli t_dilim değişkeni değiştirilmelidir.
Eğer UTC- li zaman dilimi kullanılmak istenirse time_utc -1 ile çarpılmalıdır.


örn: UTC+5, UTC+2, UTC-1

CLİENT

python3 ile çalıştırılmalıdır.
Çalıştırıldığında serverdan gelen zaman bilgisini gösterir ve saati ayarlar.