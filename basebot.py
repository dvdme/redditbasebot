import re
import praw
import queue
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import threading
import configparser
import calendar


class BaseBot:
    
    def __init__(self, bot_name, site_name, multiprocess=True):
        self._site_name = site_name
        self._bot_name = bot_name
        self.mp = multiprocess
        self.reddit = praw.Reddit(site_name=self._site_name)
        self.user_agent = self.reddit.config.user_agent
        self._setup_log()
    
    def _setup_log(self):
        self.log = logging.getLogger(self._bot_name)
        log_date_format = '%d-%m-%Y %H:%M:%S'
        if self.mp:
            log_format = logging.Formatter('[%(asctime)s] [%(name)s] [%(processName)s] [%(levelname)s] %(message)s', log_date_format)
        else:
            log_format = logging.Formatter('[%(asctime)s] [%(name)s] [%(threadName)s] [%(levelname)s] %(message)s', log_date_format)
        log_filename = '{}.log'.format(self._site_name)
        log_level = logging.DEBUG
        log_handlers = []
        log_handlers.append(TimedRotatingFileHandler(log_filename, when='midnight', interval=1, backupCount=10))
        log_handlers.append(logging.StreamHandler())
        for handler in log_handlers:
            handler.setFormatter(log_format)
            handler.setLevel(log_level)
            self.log.addHandler(handler)
        self.log.setLevel(log_level)

    def start(self):
        '''This should be implemented by other classes'''
        raise NotImplementedError

    def run(self):
        self.start()


class BotUtil:

    @staticmethod
    def get_datetime_from_unixtime(unixtime):
        return datetime.datetime.fromtimestamp(int(unixtime)).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def try_get_seconds_to_wait(ex_msg=None):
        try:
            msg = ex_msg.lower()
            search = re.search(r'\b(minutes)\b', msg)
            minutes = int(msg[search.start()-2]) + 1
            return minutes * 60
        except:
            return 60

    @staticmethod
    def get_utc_unix_timestamp():
        d = datetime.datetime.utcnow()
        unixtime = calendar.timegm(d.utctimetuple())
        return (unixtime)

    @staticmethod
    def do_reply(reply_msg, comment, log=None):
        comment.reply(reply_msg)
        if log:
            log.info('Posted reply in comment {}'.format(comment.link_permalink))
        
    @staticmethod
    def do_pm_reply(reply_title, reply_msg, redditor, log=None):
        redditor.message(reply_title, reply_msg)
        #self.log.info('Sent pm reply to {} about {}'.format(comment.author, comment.link_permalink))
        if log:
            log.info('Sent pm reply to {}'.format(redditor))

