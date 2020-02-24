from test.tests import DefaultTest

DefaultTest.run()

# todo: 3P
# SCHDULER (belli sürelerde driver tetiklemek) - buradaki parametreler mevcut testteki gibi olabilir
# - abstract, factory, vs olsun
# - primal uygula:
# -- her dakika tetiklenecek
# --- config değişmiş olabilir, tekrar oku, süre tuttuğun tabloyla merge et
# --- config.json içerisinde zamanı gelenler için
# ---- log aç
# ---- ilgili driver'ı çağır
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
# - config dosyasında tek bir scheduler olsun, onunla çalış
# - main direkt scheduler'a gitsin
# bunların parametreleri aynı klasörde mi olsun merkezi yerde mi? demo'lara parametre okumayı ekle
# tamamla
# - readme.md altına ekle
# - readme.md: yeni veri tipi ekliyorsan abstract_Database uygulamalarında da pqueue altında desteklemelisin
# sanki birden fazla attachment yaratıyor fazladan
# çok parametre alan yordamları input type'lara kır
# uygun yerlere throws try catch ekle
# log gibi işi biten queue kayıtlarını da silecek sistem düşün (notification, process, push, vs her şey bitmiş olsun)
# dışarıdan databus'e gelen bir programcı, kendi client'ını DB'sini filan verebiliyor mu? ID değil de nesne?
# hata olduğunda birilerine haber verebilmek, veya çalışırken haber almak isteyen subscriber'lar
# log da komple bir subscriber olabilir belki?
# her schedule'da klasörleri vs tekrar okuyabilsin
# lock olması lazım - aynı client için tek cycle çalışmalı. lock koyamazsan readme'ye ekle
# her processor status'ten sonra tüm attachment'ları filan tekrar yazıyor save ettiğinde, onu flag'e bağlasak?

# todo: final
# todo: factory'leri dolaş, gereksiz import'lar kalmış olabilir
# tüm factory'lerin isinstance'larına try except koy
# tüm opsiyonel parametreleri = diye çağırmış ol
# loglama diline karar ver, türkçe mi ingilizce mi olacak? ona göre tek mantıkta yürü
# todo kalmasın
# sınıfları dolaş, kullanılmamış import kalmasın
# readme gözden geçir, hatalı klasör veya eksik bilgi vs kalmasın

