# SERVER

Server Linux veya Windows bilgisayarlardan çalıştırılabilir. Çalıştığı anda IP adresini ekrana yazdırır ve 142. portu dinlemeye başlar. Çalıştığı bilgisayarın sistem saatinin doğru olması gerekmektedir. Bir istek geldiği zaman saati ms cinsinden karşıya yollar. Server başlangıç değerini sistem saati - utc saati olarak alır. UTC değerini değiştirmek için 3'e basınız. Ardından istediğiniz UTC değerini giriniz. UTC +3.5 için +0350, UTC -5 için -0500 girilmelidir. Server bu işlemi yaparken gelen isteklere de yanıt verebilir. 

**Serverı sanal makinede çalıştırmayın, IP adresini hatalı döndürüyor.**


# CLIENT

Client sadece Linux bilgisayarlar için yazılmıştır. Çalıştığında kullanıcıdan IP adresi istemektedir. IP adresi girildiğinde serverdan ms cinsinden tarih saat bilgisi gelir. Bu bilgiyi işleyip sistem saati olarak ayarlar.

**Client ile serverı aynı makinede çalıştırmayın. Serverın saati bozuluyor.**



