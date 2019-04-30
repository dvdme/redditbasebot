import re
import praw
import time
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
#import threading
import multiprocessing as mp
import threading as th
import configparser
from .basebot import BaseBot, BotUtil
from config import *
from .bot_queues import bot_queues, BotQueues
from .workers import BaseWorker


class Bot(BaseBot):

    def __init__(self, site_name, aditional_queues = None, multiprocess=True):
        super().__init__(bot_name=site_name, site_name=site_name, multiprocess=multiprocess)
        self.workers = []
        self._aditional_queues = aditional_queues
        self._queues_size_logger()

    def add_worker(self, worker):
        """
        Adds workers (watcher, filters or doers) to the bot
        :param worker: This can be a single worker or a list of workers
        :raises: TypeError
        """
        try:
            iterator = iter(worker)
        except TypeError:
            self.__add_single_worker(worker)
        else:
            for w in iterator:
                self.__add_single_worker(w)

    def __add_single_worker(self, worker):
        try:
            if isinstance(worker, BaseWorker):
                self.workers.append(worker)
                self.log.info(f'Added {str(worker)}')
            else:
                raise TypeError(f'Bot worker must derive from BaseWorker but is {type(worker)}')
        except Exception as err:
            raise err

    def start(self):
        for worker in self.workers:
            worker.setup_work()
            worker.start()

    def _queues_size_logger(self):
        size_logger_name = 'Size logger'
        def size_logger_code():
            while True:
                msg = ''
                for bq in BotQueues:
                    msg += f'{str(bq)}: {bot_queues[bq].qsize()} | '
                if self._aditional_queues:
                    for abq in self._aditional_queues:
                        msg += f'{str(abq)}: {bot_queues[abq].qsize()} | '
                self.log.info(msg.strip(' ').rstrip('|'))
                time.sleep(60)
        if self.mp:
            mp.Process(name=size_logger_name, target=size_logger_code).start()
        else:
            th.Thread(name=size_logger_name, target=size_logger_code).start()
