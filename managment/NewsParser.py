from NewsParserUtilits import NewsParser
from Clickhouse_handle import FinishedNews
from RabbitHandle import RabbitBase
from ProsExt import ProcessExt
from functools import partial
from config import NewsParserConfig
def AddToBaseByUrl(url,id,UseJs=False):
    try:
        x=NewsParser()
        info=x.parse(url,UseJs)
        base_handle=FinishedNews()
        base_handle.AddToBase(info,id)
    except Exception as e:
        print(" Исключение в addtobasebyurl",e)

def main(info):
    try:
        id=info["id"]
        url=info["payload"]
    except:
        print("warning error in input info on newsparser")
        return 0
    try:
        buf=partial(AddToBaseByUrl,url,id,NewsParserConfig.UseJs)
        x=ProcessExt([buf],1,NewsParserConfig.NewsParsTimeout)
    except:
        print("ошибка при создании партиала или экземпляра процесса")

    x.start()
    check=x.join()


    if check:
        print("Thread in addtobase was killed")


def start_main():
    x = RabbitBase("news_quere")
    x.ListenInfo(main)

if __name__=="__main__":
    x=RabbitBase("news_quere")
    x.ListenInfo(main)
    pass
