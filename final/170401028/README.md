# TCP kullanan NTP sunucu ve istemcisi

## Table of Contents

- [Nasıl Çalışır Sunucu](#about)
- [Nasıl Çalışır İstemci](#getting_started)


## Nasıl Çalışıyor : *Sunucu tarafı* <a name = "about"></a>

Sunucu tarafı python socketserver modülünü kullanıyor, bu modül sunucu yazılımlarını yazmayı kolaylaştırmak amacı ile tasarlanmış, bknz : https://docs.python.org/3/library/socketserver.html

Handler_TCP_NTP_SERVER sınıfımızı BaseRequestHandler sınıfımızdan inherit ediyoruz ve TIMEZONE değişkenimizi nesne oluşturulduğu gibi atamış oluyoruz.

````
class Handler_TCP_NTP_SERVER(socketserver.BaseRequestHandler):
    TIMEZONE = "GMT+3"
    print("Sunucu şu an ayakta ve dinliyor")
````
handle methodu BaseRequestHandlerden geliyor ve istemci tarafının requestlerine cevap vermek için bu methodu override etmeliyiz.

 istek alındıktan sonra çözülüyor ve eğer "TIMEREQUEST" mesajı yollanmışsa SEND_TIME_INFORMATION() fonksiyonu çalışıyor.

T1 = Suncunun ilk isteği aldığı anda oluşturduğu zaman damgası (buna sonra değineceğiz)
````
    def handle(self):
        T1 = datetime.datetime.now() # sunucu isteği aldığı gibi isteği aldığı zamanı kaydetti
        # self.request - TCP socketi cliente bağlı
        self.data = self.request.recv(1024).strip().decode()

        

        print("{} adresinden yollanan mesaj:".format(self.client_address[0]))

        if self.data == "TIMEREQUEST":
            self.SEND_TIME_INFORMATION(T1)
````
fonksiyon karşıya verileri bir dictionary veri yapısı olarak yolluyor, veriler

TIMEZONE = değişkende tuttuğumuz zaman dilimi

TIME = milisaniyeye çevrilmiş şu anki sunucunun saati

T1 = Sunucu isteği aldığı andaki oluşturduğu zaman damgası (datetime.datetime objesi)

T2 = Sunucu isteği tam yanıtlamadan önce oluşturduğu zaman damgası (datetime.datetime objesi)
````
def SEND_TIME_INFORMATION(self,T1):
        time_data = {
            "TIMEZONE": self.TIMEZONE,
            "TIME": float(round(time.time() * 1000)),
            "T1" : T1,
            "T2" : datetime.datetime.now()
        }
        self.request.sendall(pickle.dumps(time_data))
````

Geri kalan sunucudan bir nesne oluşturup, serve_forever() methodunu çağırmak, ve beklemek 
## Nasıl Çalışıyor : *İstemci tarafı* <a name = "getting_started"></a>

Client tarafında bir soket oluşturup ona sunucunun ip adresi ve portunu bind ediyoruz,buraları atlayıp sunucudan yanıt aldıktan sonra onu nasıl işleyeceğimize geçiyorum. Öncelikle sunucudan aldığımız zaman bize yollanan zaman milisaniye cinsinde, bunu datetime.datetime objesine donusturmek için bu methodu yazdım, bu method önce milisaniyeyi saniyeye dönüştürüp, fromtimestamp methodu ile bu hale getiriyor, bunu return edeceğiz

````
def miliseconds_to_datetime_object(self, millis):
        """
        milisecond -> datetime object
        """
        seconds = millis / 1000.0
        time = datetime.datetime.fromtimestamp(seconds)  ## şu an zaman datetime objesine dönüştü

        return time
````
Aslında her şey bu methodun içinde oluyor, öncelikle T0 yani clientin işlemi başlattığı andaki zaman damgasını alıyoruz.

Ardından sunucuya timerequest yapıyoruz bu da bize yukarda bahsettimim dictionaryi döndürüyor, buradan milisaniyeleri alıp datetime.datetime objesine dönüştürmek için fonksiyona yolluyoruz,  T1 ve T2 zaman damgaları ise sunucudan gelmiş oluyor,

bundan sonra saati ayarlamak için clientin hangi işletim sistemi üzerinde koştuğunu anlamamız gerekir, çünkü hepsi için farklı işlem yapmak gerekiyor, biz sadece linux için yapacağız, işletim sistemini öğrendikten sonra sunucudan alınan saate round_trip_delay ve offset değerlerini ekliyoruz, bunların nasıl hesaplandığına https://www.eecis.udel.edu/~mills/time.html bu linkten ulaşılabilir, 

// round trip delay gidiş geliş gecikmesi, bu değeri aldığımız saatin üzerine ekleyeceğiz
Round trip delay = (İstemci son zaman - İstemci ilk zaman) - (Sunucu son zaman + sonucu ilk zaman)

// offset değeri iki saatin vuruşları arasındaki mesela bizim saatiz serverden daha hızlı olabilir,saatimizi ne kadar hızlandıracağımızı offset değeri söylüyor., bununla işlem yapmayacağız
Offset = ((Sunucu ilk zaman - İstemci ilk zaman) + (İstemci son zaman- Sunucu son zaman)) /2

ardından *sudo date -s 'zaman'* terminal komutu ile sistem zamanını değiştireceğiz, bunun için bir subproccess başlatıp yollanan saate offset ve round trip delay eklenmiş halini *zaman* kısmına yazıp güncelliyoruz.
````
    def SET_CLOCK(self):
        """
        Önce clientin hangi işletim sistemi üzerinde koştuğunu anlayıp,
        ona göre işlem yapacağız.

        """

        T0 = datetime.datetime.now() # zaman damgası (timestamp) -0-

        request = self.send_msg_and_listen("TIMEREQUEST")  # sunucuya zamanı öğrenmek için bir istekte bulunuyoruz.
        milliseconds = request["TIME"]  # request TIMEZONE ve milisaniye cinsinden zamanı tutuyor şu an.

        #t2 ve t3 zamanları sunucudan yollanıyor
        T1 = request["T1"]
        T2 = request["T2"]

        time = self.miliseconds_to_datetime_object(milliseconds)
        plt = platform.system()

        T3 = datetime.datetime.now()

        round_trip_delay = (T3-T0) - (T2-T1) # gidiş geliş gecikmesi
        #offset =  ((T1-T0) + (T3-T2)) / 2 -ofset değerini böyle hesaplanıyor, ama bunu kullanmayacağım, belki sonra bununla da uğraşırım.
        print("Round trip delay : " + str(round_trip_delay))
        print("Offset : " + str(offset))
        if plt == "Linux":
            newdate = subprocess.Popen(["sudo", "date", "-s", str((time+round_trip_delay))])
            newdate.communicate()
            print("Saat güncellendi")

        else:
            print("Linux harici bir işletim sisteminde çalıştırıldı, çıkılıyor.")
            exit(1)
````
 


