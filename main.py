from test.tests import DefaultTest

DefaultTest().run()

# todo: 3P
# PULL klasörü: abstract + uygulama sınıfları
# PROCESS klasörü: abstract + uygulama sınıfları
# PUSH klasörü: abstract + uygulama sınıfları
# tüm bu sınıflar loga ek yapabilsin
# bunların parametreleri aynı klasörde mi olsun merkezi yerde mi?

# todo: passenger
# PASSENGER klasörü
# senkronizasyon sıklığı
# JSON: passenger tanımları
# JSON: PULL, PROCESS, PUSH listesi

# todo: driver
# konfigürasyon dosyası
# - log saklama süresi
# işlem
# - yeni log dosyası aç
# - tüm klasörlerden elindeki bilgileri tazele
# - passenger'lardan cycle'ı gelenler için 3P
# - log kaydet
# - eski log'ları sil (konfigürasyondaki süreyi geçenler)
# -- json_database içerisindeki delete_old_logs tamamlanacak
# -- bu yordamdan faydalanıp, konfigürasyonadaki süreden eski olanları sil
# - yeni cycle
