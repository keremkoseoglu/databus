from test.tests import DefaultTest

DefaultTest().run()

# todo: 3P
# PUSH klasörü: abstract + uygulama sınıfları (passenger[] ile çalış)
# müşteri hangi push'ları kullanıyor?
# PUSH: Loglama (testlere de log ekle)
# tüm bu sınıflara client yollamak iyi fikir
# bunların parametreleri aynı klasörde mi olsun merkezi yerde mi? demo'lara parametre okumayı ekle
# test altına ekle
# readme.md altına ekle

# todo: driver
# konfigürasyon dosyası
# - log saklama süresi
# işlem
# - yeni log dosyası aç
# - tüm klasörlerden elindeki bilgileri tazele
# - passenger'lardan cycle'ı gelenler için 3P (client bazında passenger aktarım sıklığıan bak JSON'dan)
# - log kaydet
# - eski log'ları sil (konfigürasyondaki süreyi geçenler)
# -- json_database içerisindeki delete_old_logs tamamlanacak
# -- bu yordamdan faydalanıp, konfigürasyonadaki süreden eski olanları sil
# - yeni cycle
# herhangi birinde hata olursa devam edip etmeme kararı?
# test altına ekle
# readme.md altına ekle
