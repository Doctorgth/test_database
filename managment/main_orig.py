from Clickhouse_handle import create_table,from_exel_to_databese
from RabbitHandle import RabbitBase
from time import sleep

def create_link_base_table():
    column_names = ["link_main", "link_news"]
    column_types = ["String", "String"]
    create_table("link_base", column_names, column_types)


def create_already_parsed_links_table():
    column_names = ["id_main_link", "link"]
    culumn_types = ["String", "String"]
    create_table("already_parsed_links", column_names, culumn_types)
    pass


def create_finished_news_table():
    column_names = ["id_main_link", "link", "title", "data_zapros", "data_news", "time_news", "text"]
    column_types = ["String", "String", "String", "String", "String", "String", "String"]
    create_table("finished_news", column_names, column_types)

    pass

def create_tables():
    create_finished_news_table()
    create_already_parsed_links_table()
    create_link_base_table()
def load_exel_to_base():
    from_exel_to_databese("exel_base")


def test(a):
    print(a)


if __name__ == "__main__":
    sleep(30)
    print("start")
    try:
        create_tables()
        try:
            load_exel_to_base()
            print("exel loaded")
        except:
            print("can't load from exel")
    except:
        print("ready")
    


