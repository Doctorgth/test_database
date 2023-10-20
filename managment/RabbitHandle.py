import pika
from functools import partial
def ListenInfoHelp(funk,ch, method, properties, body):#функция которая читает очередь и вызывает переданую ей функцию с параметром из очереди
    x=RabbitPacket()
    decoded=body.decode()
    if len(decoded)>100:
        try:
            ret = x.FromQuere(decoded)
            print("пакет успешно получен и передан в функцию")
            try:
                funk(ret)
                print("пакет был обработан функцией")
            except Exception as e:
                print("исключение при вызове связанной функции")
                print(e)
        except:
            print("warning in ListenInfo")
            print(body.decode())
    else:
        print("no url in packet with id=",decoded)
    ch.basic_ack(delivery_tag=method.delivery_tag)

class RabbitBase():#класс для взаимодействия с rabbitmq
    def __init__(self,query_name):
        self.name=query_name
        self.connection=pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    def __del__(self):
        self.connection.close()
    def SendInfo(self,info):#принимает словарь, отправляет в очередь
        x=RabbitPacket()
        packet=x.ToQuere(info)
        connection=self.connection
        channel = connection.channel()
        channel.queue_declare(queue=self.name)
        channel.basic_publish(exchange='', routing_key=self.name, body=packet)
    def ListenInfo(self,funk):# запускает прослушивание очереди
        x = RabbitPacket()
        connection = self.connection
        channel = connection.channel()
        channel.queue_declare(queue=self.name)
        ListenInfoHelp1=partial(ListenInfoHelp,funk)
        channel.basic_consume(queue=self.name, on_message_callback=ListenInfoHelp1, auto_ack=False)
        channel.start_consuming()




class RabbitPacket():# класс для преобразования словаря в строку и назад
    def __init__(self):
        pass
    def ToQuere(self,info):#принимает словарь, возвращает пакет для rabbit mq
        id=info["id"]
        id=str(id)
        while len(id)<100:# айди занимает первые 100 позиций
            id="0"+id
        main_content=""
        if type(info["payload"])==type("a"):
            main_content=info["payload"]
        else:
            for i in info["payload"]:
                buf=i+"|||"
                main_content+=buf
        return id+main_content
    def FromQuere(self,st):#возвращает пакет от представления в rabbit к словарю
        main_content=st[100:]
        id=st[:100]
        while(id[0]=="0"):
            id=id[1:]
        buf={}
        buf["id"]=id
        buf["payload"]=main_content
        return buf
        pass



