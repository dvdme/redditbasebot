import multiprocessing as mp
from enum import Enum
from config import *
from redditbasebot.bot_errors import BotError


class BotQueues(Enum):
    bot_queue_unfiltered = 0
    bot_queue_filtered = 1
    bot_queue_retry = 2
    #Add more queues as needed here

bot_queues = {}

for bot_queue in BotQueues:
    bot_queues[bot_queue] = mp.Queue(QUEUE_MAX_SIZE)

def add_new_queue(bot_queue_enum):
    if bot_queue_enum in BotQueues:
        try:
            raise BotError(f'Can not add new queue with enum {bot_queue_enum}. Create a new custom enum to identify new queues')
        except BotError as boterr:
            raise boterr
    bot_queues[bot_queue_enum] = mp.Queue(QUEUE_MAX_SIZE)
