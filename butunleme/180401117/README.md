
Hedefe ICMP (Internet Control Message Protocol) paketleri göndererek hedefin yolunun bulunması sağlanır. 
Yazdığım rota.py programı TTL (Time To Live) değerlerini kullanarak çalışmaktadır. Yol üzerinde bulunan her IP TTL süresini 1 değer düşürerek kaç yönlendiriciden geçildiğini gösterir. Aradaki yönlendiricilerin bazılarında “Request time out” şeklinde mesaj verebilir. Bu zaman aşımına uğramış TTL paketleridir. Bu yönlendirici tarafından kendini gizleme olarak düşünebilirsiniz. Sadece ICMP paketlerine cevap vermiyordur.

Çalıştırılması için aşağıdaki komut çalıştırmak yeterlidir:

# sudo rota.py github.com

Çıktısı da rota.txt dosyanın içine yazılmaktadır.
