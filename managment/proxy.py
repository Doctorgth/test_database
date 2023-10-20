import random
def get_proxy():
    f=open("proxy_list.txt","r")
    k=f.readlines()
    f.close()
    i=random.randint(0,len(k))
    try:
        ret=k[i]
        ret=ret.replace("\n","")
        ret=ret.replace(" ","")
        return ret
    except:
        print("при попытке выдать прокси что то пошло не так")