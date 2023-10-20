from time import sleep, time
from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from proxy import get_proxy
from config import UsingProxeConfig
use_proxy=UsingProxeConfig.useproxy
def set_use_proxy(value):# если поставить True то подключение всех страниц через классы этого файла будет по прокси
    global use_proxy
    use_proxy=value

class NewsParser:  # класс который по конкретной ссылке на новость
    def __init__(self):  # тянет из неё словарь
        pass

    def parse(self, url, Use_Js=False):  # создает словарьь по ссылке
        ret = {}
        print("now parsing url=",url)
        try:
            if Use_Js:
                soup = self.create_soup_js(url)
            else:
                soup = self.create_soup(url)
            title = soup.find("title")
            title = title.text.replace("\n", " ")
        except:
            ret["link"] = url
            ret["title"] = "Error"
            ret["data_zapros"] = str(time())
            ret["data_news"]=""
            ret["time_news"]=""
            ret["text"]=""
            return ret
        try:
            ret["link"] = url
            ret["title"] = title
            ret["data_zapros"] = str(time())
            d = find_date_on_new_page(soup)
            if len(d) > 0:
                if ":" in d[0]:
                    ret["date_news"] = d[0]
                    ret["time_news"] = d[0]
                else:
                    ret["date_news"] = d[0]
                    t = find_time_on_new_page(soup)
                    if len(t) > 0:
                        ret["time_news"] = t[0]
                    else:
                        ret["time_news"] = "NotFound"
            else:
                ret["date_news"] = "NotFound"
                ret["time_news"] = "NotFound"
            ret["text"] = soup.get_text()
            #ret["content"] = soup.prettify()
            return ret
        except:
            ret["link"] = url
            ret["title"] = "Error"
            ret["data_zapros"] = str(time())
            ret["data_news"] = ""
            ret["time_news"] = ""
            ret["text"] = ""
            return ret

    def create_soup(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def create_soup_js(self, url):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        global use_proxy
        if use_proxy:
            chrome_options.add_argument('--proxy-server=' + get_proxy())
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        if use_proxy:
            sleep(20)
        sleep(5)
        html = driver.page_source

        driver.quit()

        soup = BeautifulSoup(html, "html.parser")
        return soup


def check_string_is_time(st):  # вспомогательная функция, проверяет содержит ли строка время
    k = st.find(":")
    if st[k - 1].isdigit() and st[k + 1].isdigit():
        return True
    if st[k - 1] == " " and st[k + 1] == " ":
        if st[k - 2].isdigit() and st[k + 2].isdigit():
            return True
    return False
    pass


def find_time_on_new_page(soup):  # анализирует страницу в поисках времени на ней
    all_text = soup.get_text()  # возвращает массив из всего найденного времени на странице
    mas = all_text.split("\n")
    mas1 = []
    for i in mas:
        if i != "" and ":" in i:
            if check_string_is_time(i):
                mas1.append(i)
    return mas1


def check_allow_in_str(st, allow_mas):  # проверяет строку на содержание в ней ключевых слов
    for i in allow_mas:
        if i in st:
            return True, i
    return False, 0


def check_string_is_date(st, word_triger):  # проверяет строку на содержание в ней даты
    k = st.find(word_triger)
    l = len(word_triger)
    assert k != -1  # Подаваемое слово должно быть в строке
    if st[k - 1] == " " and st[k - 2].isdigit():
        if st[k + l] == " " and st[k + l + 1].isdigit():
            return True

    return False


def find_date_on_new_page(soup):  # ищет все даты на странице, возвращает массив дат
    all_text = soup.get_text()
    mas = all_text.split("\n")
    mas1 = []
    allow_w = ["января", "февраля", "марта",
               "июня", "июля", "августа",
               "сентября", "октября", "ноября",
               "декабря", "апреля", "мая"]
    for i in mas:
        if i != "":
            check_buf = check_allow_in_str(i, allow_w)
            if check_buf[0]:
                if check_string_is_date(i, check_buf[1]):
                    mas1.append(i)
    return mas1

