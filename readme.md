# Databüs

## Konfigürasyon
Yeni bir yere kopyalandığında:
* config/constants.py dosyasını güncelleyip, doğru değerleri barındırdığından emin olun.

Yeni bir müşteri geldiğinde (ismi abc olsun):
* json_db/clients/abc klasörünü oluşturun
- Bu klasörün altına, json_db/clients/demo klasör / dosya yapısının aynısını oluşturun

## Geliştirme
Yeni bir işlev eklendiğinde;
* test/tests.py dosyasına bu işlev ile ilgili bir test eklemekte fayda var

## Test
test/test.py dosyasındaki testleri yürüterek, sistemin sağlıklı işleyip işlemediğini görebilirsiniz.