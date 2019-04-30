import time
import multiprocessing as mp
import threading as th
from config import *
from .basebot import BotUtil


class BaseWorker:

    def __init__(self, bot, name, worker_sleep_time = 1):
        self.name = name
        self.reddit = bot.reddit
        self.log = bot.log
        self.mp = bot.mp
        if self.mp:
            self.process = None
        else:
            self.thread = None
        self.worker_sleep_time = worker_sleep_time

    def loop_code(self, start_sleep_time, worker_code):
        while True:
            time_to_sleep = start_sleep_time
            try:
                worker_code()
            except Exception as ex_msg:
                self.log.exception(ex_msg)
            finally:
                time.sleep(time_to_sleep)
        
    def start(self):
        if self.mp:
            self.process.start()
        else:
            self.thread.start()

    def setup_work(self):
        self.log.info(f'Started {self.name}')
        args = (self.worker_sleep_time, self.worker_logic)
        if self.mp:
            self.process = mp.Process(name=self.name, target=self.loop_code, args=args)
        else:
            self.thread = th.Thread(name=self.name, target=self.loop_code, args=args)

    def worker_logic(self):
        '''This should be implemented by other classes'''
        raise NotImplementedError
    
    def __str__(self):
        return f'Bot name: {self.name} | Multiprocess: {self.mp} | Worker sleep time {self.worker_sleep_time} | reddit instance {str(self.reddit)}'


class Watcher(BaseWorker):

    def __init__(self, bot, watcher_name = 'Watcher'):
        super().__init__(bot, name=watcher_name, worker_sleep_time=WATCHER_TIME_TO_SLEEP)

class Filter(BaseWorker):

    def __init__(self, bot, filter_name = 'Filter'):
        super().__init__(bot, name=filter_name, worker_sleep_time=FILTER_TIME_TO_SLEEP)


class Doer(BaseWorker):

    def __init__(self, bot, doer_name = 'Doer'):
        super().__init__(bot, name=doer_name, worker_sleep_time=DOER_TIME_TO_SLEEP)
