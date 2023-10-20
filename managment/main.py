from time import sleep, time
from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


use_proxy = False


def set_use_proxy(value):  # если поставить True то подключение всех страниц через классы этого файла будет по прокси
    global use_proxy
    use_proxy = value


class NewsParser:  # класс который по конкретной ссылке на новость
    def __init__(self):  # тянет из неё словарь
        pass

    def parse(self, url, Use_Js=False):  # создает словарь по ссылке
        ret = {}
        print("now parsing url=", url)
        if True:
            if Use_Js:
                print("try create soup js")
                soup = self.create_soup_js(url)
                print("create soup js compplete")
                print("TEXT=",soup.text)
            else:
                print("try create no js soup")
                soup = self.create_soup(url)
                print("complete create no js soup")


    def create_soup(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def create_soup_js(self, url):
        """
        chrome_options = Options()
        print
        chrome_options.add_argument("--headless")
        
        chrome_options.add_argument('--no-sandbox')
        global use_proxy
        if use_proxy:
            chrome_options.add_argument('--proxy-server=' + get_proxy())
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        if use_proxy:
            sleep(UsingProxeConfig.delay_if_use_active)
        sleep(UsingProxeConfig.delay_browzer)
        html = driver.page_source

        driver.quit()

        soup = BeautifulSoup(html, "html.parser")
        return soup
        """
        chrome_options = Options()
        # chrome_options.add_argument('--proxy-server=143.244.60.116:844


        # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

        chrome_options.add_argument("--headless")
        # chrome_options.add_argument('--user-agent={0}'.format(user_agent))
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.binary_location = '/ opt / headless-chromium'
        print("before driver select")
        driver = webdriver.Remote(
    command_executor='http://localhost:4443/wd/hub',options=chrome_options
    
)
        #driver = webdriver.Chrome(options=chrome_options)
        print("before .get url", url)
        driver.get(url)
        print("after get url")

        print("before sleep")

        print("berore driver.page_sourse")
        html = driver.page_source
        print("after page sourse")


        driver.quit()

        soup = BeautifulSoup(html, "html.parser")
        return soup




x=NewsParser()
x.parse("https://archeage.ru/news/316662.html",True)
