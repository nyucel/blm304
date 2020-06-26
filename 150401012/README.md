150401012 Yiğit Yüre

Komut satırında "sudo python3 rota.py hedef_adres" olacak şekilde ulaşılmak istenilen adres girilir.
Yönlendiricilere ulaşmak için soket oluşturulur. Paket göndermek için UDP, almak için ICMP kullanılır.
Yönlendirici aldığı UDP paketindeki hedef adresin kendisi olup olmadığını kontrol eder ve geriye ICMP paketi gönderir. Eğer hedef_adres kendisi değilse balka bir yönlendiriciye paket gönderir, ttl 1 arttırılır.
Ana makineden sonra paket, en fazla 30 yönlendiriciye ulaşabilir. ttl 30 olduktan sonra paket düşürülür.
Her yönlendiriciden geçişte ekrana ttl numarasıyla birlikte yönlendirici adresi ve adresin ismi yazılır. Ayrıca rota.txt adlı dosyaya yönlendiricinin adresi yazılır.
hedef_adres'e ulaşıldığında rota.txt dosyası kapatılır ve program sonlanır.
