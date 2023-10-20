import sqlite3

base_name = "DataBase.db"
import openpyxl
#Старый файл для работы с sqlite3

def create_table(table_name, column_names, column_types):
    connection = sqlite3.connect(base_name)
    cursor = connection.cursor()
    zapros = "CREATE TABLE " + table_name + " ("
    l_names = len(column_names)
    assert l_names == len(column_types)
    for i in range(l_names):
        column = column_names[i] + " " + column_types[i]
        zapros += column + ", "
    zapros = zapros[:-2]
    zapros += ")"
    cursor.execute(zapros)
    connection.commit()
    connection.close()


class TableHandle():#класс для работы с sql таблицами а так же набор доп классов для конкретных таблиц
    def __init__(self, table_name):
        self.table_name = table_name
        self.connection = sqlite3.connect(base_name)

    def __del__(self):
        self.connection.close()


class LinkBase(TableHandle):  # Таблица с ссылками на основные сайты откуда тягаются новости
    def __init__(self):
        self.table_name = "link_base"
        self.connection = sqlite3.connect(base_name)

    def add_info(self, mas_info):
        cursor = self.connection.cursor()
        for i in mas_info:
            zapros = "INSERT INTO " + self.table_name + " (link_main, link_news) VALUES ('" + i["link_main"] + "', '" + \
                     i["link_news"] + "')"
            cursor.execute(zapros)
        self.connection.commit()

    def get_links(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT id,link_news FROM ' + self.table_name)
        rows = cursor.fetchall()

        ret = []
        for i in rows:
            buf = {}
            buf["id"] = i[0]
            buf["links"] = i[1]
            ret.append(buf)
        return ret

        pass

    def get_links_by_id(self, id):  # воззвращает ссылки связанные с конкретным сайтом
        cursor = self.connection.cursor()
        cursor.execute('SELECT id,link_news FROM ' + self.table_name + " WHERE id=?", (id,))
        rows = cursor.fetchall()

        ret = []
        for i in rows:
            buf = {}
            buf["id"] = i[0]
            buf["links"] = i[1]
            ret.append(buf)
        return ret


def from_exel_to_databese(base_patch):
    base = openpyxl.load_workbook(base_patch + ".xlsx")
    mass_to_add = []
    sheet = base.active

    # cell_value = sheet['A1'].value
    for i in range(3, 328):
        value = sheet["B" + str(i)].value
        if value is not None:
            if value.startswith("http"):
                buf = {}
                buf["link_main"] = value
                link_news = sheet["H" + str(i)].value
                if link_news is not None:
                    buf["link_news"] = link_news
                else:
                    buf["link_news"] = ""
                mass_to_add.append(buf)
    x = LinkBase()
    x.add_info(mass_to_add)


class AlreadyLinks(TableHandle):  # таблица где хранятся уже известные ссылки (для удаления дубликатов)
    def __init__(self):
        self.table_name = "already_parsed_links"
        self.connection = sqlite3.connect(base_name)

    def GetLinksById(self, id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT link FROM ' + self.table_name + " WHERE id_main_link=?", (id,))
        rows = cursor.fetchall()
        return rows

    def AddUrls(self, urls, id):
        cursor = self.connection.cursor()
        for i in urls:
            try:

                zapros = "INSERT INTO " + self.table_name + " (id_main_link, link_news) VALUES (" + id + ", '" + i + "')"#колонка называется не link_news а просто links
            except:
                print("ошибка при составлении запроса")
                print("type id=",type(id),"type i=",type(i))
            try:
                cursor.execute(zapros)
            except Exception as e:
                print(" не удалось сделать запрос")
                print("zapros=",zapros)
                print(e)
        self.connection.commit()


def RemoveSpesSymvol(text):
    text = text.replace("`", '"')
    text = text.replace("'", '"')
    text = text.replace(";", " ")
    text = text.replace("OR", " ")
    text = text.replace("AND", "")
    text = text.replace("&", "")
    text = text.replace("|", "")

    return text


class FinishedNews(TableHandle):
    def __init__(self):
        self.table_name = "finished_news"
        self.connection = sqlite3.connect(base_name)

    def AddToBase(self, info, id_main_link):
        cursor = self.connection.cursor()
        i = info
        text = i["text"]
        text = text.replace("\n\n", ".")
        text = text.replace("\n\n", ".")
        text=RemoveSpesSymvol(text)
        zapros = "INSERT INTO " + self.table_name + " (id_main_link,link,title,data_zapros,data_news,time_news,text) VALUES ('" + id_main_link + "','" + \
                 i["link"] + "','" + i["title"] + "','" + i["data_zapros"] + "','" + i["date_news"] + "','" + i[
                     "time_news"] + "','" + text + "')"
        cursor.execute(zapros)
        self.connection.commit()

        #

        pass
