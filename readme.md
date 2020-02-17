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

Yeni bir veritabanına geçmek isterseniz;
* database/ altında abstract_database'den yeni bir sınıf türetin ve yordamlarını değiştirin
* database/factory içerisinde yeni veritabanını döndürün

## Test
test/test.py dosyasındaki testleri yürüterek, sistemin sağlıklı işleyip işlemediğini görebilirsiniz.

Yeni bir işlev eklendiğinde; test/tests.py dosyasına bu işlev ile ilgili bir test eklemekte fayda var