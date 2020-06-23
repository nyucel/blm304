# Veri Haberleşmesi Dersi - Büt Ödevi

Rabia Kaynak - 160401091

python3 ile traceroute benzeri bir uygulama.
## Kullanılan Ek Kütüphane

Scapy, dokümantasyona [buradan](https://scapy.readthedocs.io/en/latest/)
 ulaşabilirsiniz.

```bash
sudo pip3 install scapy
```
şeklinde yükledim.

## Kullanım

Aşağıdaki şekilde kullanılıyor. Çıktıları **rota.txt** dosyasına yazdırıyor.

```bash
sudo python3 rota.py site.com
```
### Nereye yazılıyor?
rota.txt dosyası aşağıdaki şekilde görünmekte. 30 ile sınırlanmış durumda.
```bash
Site: www.comu.edu.tr
TTL: 1, IP 10.0.2.2
TTL: 2, IP 192.168.43.96
TTL: 3, IP 10.182.182.154
TTL: 4, IP 10.182.182.154
TTL: 5, IP 10.182.182.129
TTL: 6, IP 10.182.10.37
TTL: 7, IP 10.182.10.38
TTL: 8, IP 10.134.100.10
TTL: 9, IP 10.134.100.9
TTL: 10, IP 46.234.28.94
TTL: 11, IP 46.234.28.101
TTL: 12, IP 31.145.74.161
TTL: 13, IP 81.8.12.82
TTL: 14, IP 193.255.0.14
```


## Güncellemeler
23.06.2020 - İlk.