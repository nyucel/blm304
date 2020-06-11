# Veri Haberleşmesi

Veri Haberleşmesi Dersi 2019 - 2020 Final Ödevi

## Bilgiler

İki makineyi aynı NAT ağında bağlayıp haberleştiklerini test ettim. IP adresleri aşağıdaki gibidir.

**Server IP**: 10.0.2.4

**Client IP**: 10.0.2.15

Öncelikle Client ve Server makineden tüm portları aşağıdaki IPTABLES komutlarını kullanarak kapattım. Yalnızca TCP 142. port açık.

```bash
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

iptables -A INPUT -p tcp --dport 142 -j ACCEPT
```

## Kullanım
### Server Tarafında
İşletim sistemi olarak sanal makine olarak Ubuntu 20.04 versiyonunu kullandım. Python 3  ile aşağıdaki şekilde server'ı başlatıyoruz.
```bash
sudo python3 time_zone_server.py
```
Sonrasında Server makinedeki zaman dilimini değiştirmek isteyip istemediğimizi belirliyoruz.
```bash
Do u want to change current timezone? - Current [UTC +00] (y/n)
> y
```
Bizden zaman dilimi girmemizi istiyor. İstediğimiz zaman diliminin belirliyoruz.
```bash
Set UTC timezone (ex. +03)
> +03
```
Daha sonra Serve bağlantıları dinlemeye başlıyor ve bağlantıyı Client makineden yapıyoruz.
```bash
Server Listening ...
Connection address: 10.0.2.15
```
### Client Tarafı
İşletim sistemi olarak sanal makine olarak Ubuntu 20.04 versiyonunu kullandım. Python 3  ile aşağıdaki şekilde Client'ı başlatıyoruz.
```bash
sudo python3 time_zone_client.py
```
Sonrasında Client makinedeki zaman dilimini bize yazdırıyor. Daha sonra komutları listeliyor.
```bash
Current UTC: +03
/*------Commands:-----*/
GET: Get timezone from server 
SET: Set timezone
/*--------------------*/

Your Input:

>GET
```

GET komutunu girdiğimizde Server'ın zaman dilimini Client'a atamış oluyoruz. Daha sonra bunu yazdıyoruz.
```bash
UTC +02
```

SET komutunu girdiğimizde ise Client'ın zaman dilimini Server'a atamış oluyoruz.