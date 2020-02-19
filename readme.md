# Databüs

## Konfigürasyon
Yeni bir yere kopyalandığında:
* config/constants.py dosyasını güncelleyip, doğru değerleri barındırdığından emin olun.

Yeni bir müşteri geldiğinde (ismi abc olsun):
* json_db/clients/abc klasörünü oluşturun
- Bu klasörün altına, json_db/clients/demo klasör / dosya yapısının aynısını oluşturun

## Geliştirme
Geliştirme standartları:
* Abstract sınıflara ait dosyalar, abstract_ adıyla başlamalıdır.
* Yeni sınıf döndüren dosyalar, factory.py diye adlandırılmalıdır

Yeni bir veri türü eklemek isterseniz;
* passenger/ altına abstract_passenger 'den yeni bir sınıf türetin
* Bu sınıfa ait dosyada tek bir sınıf olmalıdır, o da Abstract Class'ten türetilen sınıf olmalıdır
* Sınıfın __init__ 'inde Super'i çağırmayı unutmayın. Örnek olarak Demo'lara bakabilirsiniz.
* Bu veri türüyle ilgili Puller / Processor / Pusher sınıfı eklemeniz gerekebilir

Yeni bir veri okuyucu eklemek isterseniz;
* Veri türü henüz yoksa, yeni bir Passenger ekleyin
* puller/ altına abstract_puller 'dan yeni bir sınıf türetin
* Bu sınıfa ait dosyada tek bir sınıf olmalıdır, o da Abstract Class'ten türetilen sınıf olmalıdır
* Bu okuyucu hangi Client'larda çalışacaksa, o Client'ların konfigürasyonuna eklenmelidir. Örnek: json_db/clients/demo/config.json altına ekleyebilirsiniz.

Yeni bir veri işlemcisi eklemek isterseniz;
* Veri türü henüz yoksa, yeni bir Passenger ekleyin
* processor/ altına abstract_processor 'dan yeni bir sınıf türetin
* Bu sınıfa ait dosyada tek bir sınıf olmalıdır, o da Abstract Class'ten türetilen sınıf olmalıdır
* Sınıfın __init__ 'inde Super'i çağırmayı unutmayın. Örnek olarak Demo'lara bakabilirsiniz.
* Bu okuyucu hangi Client'larda çalışacaksa, o Client'ların konfigürasyonuna eklenmelidir. Örnek: json_db/clients/demo/config.json altına ekleyebilirsiniz.

Yeni bir veri gönderici eklemek isterseniz;
* Veri türü henüz yoksa, yeni bir Passenger ekleyin
* pusher/ altına abstract_pusher 'dan yeni bir sınıf türetin
* Bu sınıfa ait dosyada tek bir sınıf olmalıdır, o da Abstract Class'ten türetilen sınıf olmalıdır
* Bu okuyucu hangi Client'larda çalışacaksa, o Client'ların konfigürasyonuna eklenmelidir. Örnek: json_db/clients/demo/config.json altına ekleyebilirsiniz.

Yeni bir veritabanına geçmek isterseniz;
* database/ altında abstract_database'den yeni bir sınıf türetin ve yordamlarını değiştirin
* config/constants.py dosyasındaki DATABASE_MODULE değerini değiştirin

## Test
test/test.py dosyasındaki testleri yürüterek, sistemin sağlıklı işleyip işlemediğini görebilirsiniz.

Yeni bir işlev eklendiğinde; test/tests.py dosyasına bu işlev ile ilgili bir test eklemekte fayda var