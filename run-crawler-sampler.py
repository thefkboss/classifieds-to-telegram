"""
This is another example how to use the crawlers using a list of pairs (url, chat_id) to setup them
"""

from settings import TELEGRAM_TOKEN, BOT_CHAT_ID, CHECKING_TIMEOUT, TYPE_URL_N_CHAT
from telegram_writer import TelegramWriter

if __name__ == '__main__':
    bots = []
    for CrawlerInstance, urls_n_chats in TYPE_URL_N_CHAT.items():
        for url, chat_id in urls_n_chats:
            bots.append(CrawlerInstance(url, chat_id))
    telegram = TelegramWriter(TELEGRAM_TOKEN, BOT_CHAT_ID or None)
    telegram.run(bots, wait_seconds=CHECKING_TIMEOUT)