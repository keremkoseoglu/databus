from config.constants import *
from database.primal_factory import PrimalDatabaseFactory
from dispatcher.abstract_factory import DispatcherTicket
from dispatcher.primal_factory import PrimalDispatcherFactory
from driver.primal_factory import PrimalDriverFactory
from passenger.primal_factory import PrimalPassengerFactory
from pqueue.primal_factory import PrimalQueueFactory
from puller.primal_factory import PrimalPullerFactory
from pusher.primal_factory import PrimalPusherFactory
from processor.primal_factory import PrimalProcessorFactory
from test.tests import DefaultTest


def run_live():
    dispatcher_ticket = DispatcherTicket(
        p_database_factory=PrimalDatabaseFactory(),
        p_driver_factory=PrimalDriverFactory(),
        p_passenger_factory=PrimalPassengerFactory(),
        p_queue_factory=PrimalQueueFactory(),
        p_puller_factory=PrimalPullerFactory(),
        p_processor_factory=PrimalProcessorFactory(),
        p_pusher_factory=PrimalPusherFactory(),
        p_database_module=DATABASE_DEFAULT,
        p_driver_module=DRIVER_DEFAULT)

    PrimalDispatcherFactory().create_dispatcher(
        p_module=DISPATCHER_DEFAULT,
        p_ticket=dispatcher_ticket).start()


def run_test():
    DefaultTest.run()


run_live()

# todo: 3P
# dispatcher eski logları sildiği gibi eski ve işi biten queue'ları da silsin (notification, process, push, vs her şey bitmiş olsun)
# - altyapı tamamla
# - dispatcher'dan yordamı çağır
# sanki birden fazla attachment yaratıyor fazladan
# çok parametre alan yordamları input type'lara kır
# dışarıdan databus'e gelen bir programcı, kendi client'ını DB'sini filan verebiliyor mu? ID değil de nesne? bunu örnek bir dış proje ile dene
# hata olduğunda birilerine haber verebilmek, veya çalışırken haber almak isteyen subscriber'lar
# log da komple bir subscriber olabilir belki?
# lock olması lazım - aynı client için tek cycle çalışmalı. lock koyamazsan readme'ye ekle
# her processor status'ten sonra tüm attachment'ları filan tekrar yazıyor save ettiğinde, onu flag'e bağlasak?

# todo: final
# todo: factory'leri dolaş, gereksiz import'lar kalmış olabilir
# tüm factory'lerin isinstance'larına try except koy
# tüm opsiyonel parametreleri = diye çağırmış ol
# loglama diline karar ver, türkçe mi ingilizce mi olacak? ona göre tek mantıkta yürü
# __ geçenleri _ ile değiştir kodda
# todo kalmasın
# sınıfları dolaş, kullanılmamış import kalmasın
# config.constants hala lazım mı? onu bir json yapsak?
# readme gözden geçir, hatalı klasör veya eksik bilgi vs kalmasın

