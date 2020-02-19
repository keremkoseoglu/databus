from test.tests import DefaultTest

DefaultTest().run()

# todo: 3P
# artık driver'ı yazma vakti.
# # - yapıyı aç
# - factory, prime_driver filan olsun.
# - müşteri'deki passenger driver seçebilsin.
# - her driver, sadece kendi passenger'ları üzerinde işlem yapsın
# test yerine buradan driver içinden demo yürüt
# QUEUE
# - pqueue'ya yazdıklarını pull'da' "mark as read" diye döndürebiliyor olmalısın
# -- sınıflara ekle
# -- teste ekle
# - push'a pqueue'dan gelenleri yolla
# - pusher geriye başarılı / başarısız olanları döndürebilmeli, ona göre pqueue güncelle
# -- sınıflara ekle
# -- teste ekle
# - readme.md

# bunların parametreleri aynı klasörde mi olsun merkezi yerde mi? demo'lara parametre okumayı ekle
# tamamla
# - test altına ekle
# - readme.md altına ekle
# - readme.md: yeni veri tipi ekliyorsan abstract_Database uygulamalarında da pqueue altında desteklemelisin

# todo: driver
# konfigürasyon dosyası
# - log saklama süresi
# işlem
# - yeni log dosyası aç
# - tüm klasörlerden elindeki bilgileri tazele
# - passenger'lardan cycle'ı gelenler için 3P (client bazında passenger aktarım sıklığıan bak JSON'dan) + QUEUE
# - pqueue'ya yazdığını pull ile OK diye işaretle
# - push ettiklerini pqueue'da güncelle
# - log kaydet
# - işi bitmiş eski pqueue'ları sil (konfigürasyondaki süreyi geçenler - yeni süre ekle)
# - eski log'ları sil (konfigürasyondaki süreyi geçenler)
# -- json_database içerisindeki delete_old_logs tamamlanacak
# -- bu yordamdan faydalanıp, konfigürasyonadaki süreden eski olanları sil
# - yeni cycle
# herhangi birinde hata olursa devam edip etmeme kararı?
# lock olması lazım - aynı client için tek cycle çalışmalı. lock koyamazsan readme'ye ekle
# test altına ekle
# readme.md altına ekle

# todo: final
# loglama diline karar ver, türkçe mi ingilizce mi olacak? ona göre tek mantıkta yürü
# todo kalmasın

