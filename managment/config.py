class DatabaseConfig():
    host = "clickhouse"
    username = "admin"
    password = 'admin'
    database = "test"

class NewsParserConfig():
    UseJs=False#запускать ли браузер при парсинге сайта
    NewsParsTimeout=40# максимальное время которое парсер может обрабатывать 1 новость из очереди

class UsingProxeConfig():
    useproxy=False
    delay_if_use_active=20# включенное прокси увеличивает время на подключение, это время дополнительного ожидания(суммируется с основным)
    delay_browzer=5#время ожидания прогрузки страницы до  получения с неё кода
class LinkGeneratorConfig():
    thread_count_max=10#максимальное число потоков которые будут одновременно парсить ссылки
    thread_timeout=50#суммарное время ожидание на работу одного потока( на самом деле thread_delay*число_потоков+thread_timeout для первого и thread_timeout для последнего)
    thread_delay=4#промежуток между запусками потоков
    period_delay=60 # время в минутах между стягиванием новостных ссылок
