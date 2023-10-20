from threading import Thread
from multiprocessing import Process
from time import time,sleep
from functools import partial
class ThreadExt():
    def __int__(self,funk,timeout):
        self.funk=funk
        self.timeout=timeout
    def start(self):
        self.thread=Thread(target=self.funk)
        self.time=time()
        self.time_end=self.time+self.timeout
    def check_timeout(self):
        if time()>self.time_end:
            if self.thread.isAlive():
                self.thread.kill()

def thread_funk(mass,delay):
    for i in mass:
        t=Thread(target=i)
        t.start()
        sleep(delay)


class ProcessExt():#Класс который в отдельном процессе запускает набор потоков, поддерживает таймаут
    def __init__(self,mass_f,thread_delay,timeout):
        self.mass_f=mass_f
        self.delay=thread_delay
        self.timeout=timeout+len(mass_f)*thread_delay
        pass
    def start(self):
        self.proc=Process(target=partial(thread_funk,self.mass_f,self.delay))
        self.proc.start()
        self.time_start=time()
    def is_alive(self):
        return self.proc.is_alive()
    def join(self):
        time_end=self.time_start+self.timeout
        while self.is_alive():
            if time()>time_end:
                self.proc.kill()
                return True
            sleep(1)
        return False
