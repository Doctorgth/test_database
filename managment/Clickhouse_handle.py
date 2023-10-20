import clickhouse_connect
import openpyxl
from config import DatabaseConfig
host=DatabaseConfig.host
username=DatabaseConfig.username
password=DatabaseConfig.password
database=DatabaseConfig.database


def create_table(table_name,column_names,column_types):
    assert len(column_names)==len(column_types)
    global host,username,password
    client = clickhouse_connect.get_client(database=database,host=host, username=username, password=password)
    zapros = "CREATE TABLE " + table_name + " ("
    l_names = len(column_names)
    assert l_names == len(column_types)
    for i in range(l_names):
        column = column_names[i] + " " + column_types[i]
        zapros += column + ", "
    zapros = zapros[:-2]
    zapros += ")"+" ENGINE MergeTree ORDER BY "+column_names[0]
    client.command(zapros)



class LinkBase:  # Таблица с ссылками на основные сайты откуда тягаются новости
    def __init__(self):
        self.table_name = "link_base"
        self.connection = clickhouse_connect.get_client(database=database,host=host, username=username, password=password)

    def add_info(self, mas_info):
        client = self.connection
        client.insert(self.table_name,mas_info,column_names=["link_main", "link_news"])


    def get_links(self):
        client = self.connection
        ret=client.query("SELECT link_main,link_news FROM "+self.table_name)
        rows=ret.result_rows


        ret = []
        for i in rows:
            buf = {}
            buf["id"] = i[0]
            buf["links"] = i[1]
            ret.append(buf)
        return ret

        pass


    def get_links_by_id(self, id):  # воззвращает ссылки связанные с конкретным сайтом
        cursor = self.connection
        ret=cursor.query('SELECT link_main,link_news FROM ' + self.table_name + " WHERE (link_main=='"+id+"')")
        rows = ret.result_rows

        ret = []
        for i in rows:
            buf = {}
            buf["id"] = i[0]
            buf["links"] = i[1]
            ret.append(buf)
        return ret



def show_table(table_name):
    client = clickhouse_connect.get_client(database=database,host=host, username=username, password=password)
    ret=client.query("SHOW CREATE TABLE "+table_name)
    print(ret.result_rows)


class AlreadyLinks:  # таблица где хранятся уже известные ссылки (для удаления дубликатов)
    def __init__(self):
        self.table_name = "already_parsed_links"
        self.connection = clickhouse_connect.get_client(database=database,host=host, username=username, password=password)

    def GetLinksById(self, id):
        cursor = self.connection
        ret=cursor.query('SELECT link FROM ' + self.table_name + " WHERE (id_main_link=='"+id+"')")
        rows = ret.result_rows
        return rows

    def AddUrls(self, urls, id):
        client= self.connection
        mas_info=[]
        for i in urls:
            mas_info.append([id,i])
        try:
            client.insert(self.table_name, mas_info, column_names=["id_main_link", "link"])
        except:
            print("error при попытке занести ссылки в уже известные")

def RemoveSpesSymvol(text):#минимальная защита от sql инъекций
    text = text.replace("`", '"')
    text = text.replace("'", '"')
    text = text.replace(";", " ")
    text = text.replace("OR", " ")
    text = text.replace("AND", "")
    text = text.replace("&", "")
    text = text.replace("|", "")

    return text


class FinishedNews:# таблица обработанных новостей
    def __init__(self):
        self.table_name = "finished_news"
        self.connection = clickhouse_connect.get_client(database=database,host=host, username=username, password=password)

    def AddToBase(self, info, id_main_link):
        print("we are in add to base")
        client = self.connection
        print("connect true")
        i = info
        text = i["text"]
        text = text.replace("\n\n", ".")
        text = text.replace("\n\n", ".")
        text=RemoveSpesSymvol(text)
        print("before zapros")
        if i["data_news"]==None:
          i["data_news"]=""
          print("data in news is none")
        if i["time_news"]==None:
          i["time_news"]=""
        zapros = [[id_main_link,i["link"],i["title"],i["data_zapros"],i["data_news"],i["time_news"],text]]
        #print("zapros=",zapros)
        client.insert(self.table_name, zapros, column_names=["id_main_link","link","title","data_zapros","data_news","time_news","text"])
        

        #

        pass















def from_exel_to_databese(base_patch):
    base = openpyxl.load_workbook(base_patch + ".xlsx")
    mass_to_add = []
    sheet = base.active

    # cell_value = sheet['A1'].value
    for i in range(3, 328):
        value = sheet["B" + str(i)].value
        if value is not None:
            if value.startswith("http"):
                buf = []
                buf.append(value)
                link_news = sheet["H" + str(i)].value
                if link_news is not None:
                    buf.append(link_news)
                else:
                    buf.append("")
                mass_to_add.append(buf)
    x = LinkBase()
    x.add_info(mass_to_add)
