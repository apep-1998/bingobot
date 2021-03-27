from telegram.ext import Updater
from routers import routers_list
import settings


if __name__ == '__main__':
    updater = Updater(settings.token)

    for r in routers_list:
        updater.dispatcher.add_handler(r)
    updater.start_polling()
    updater.idle()
