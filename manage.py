from telegram.ext import Updater
from views import views
from controllers import controllers
from routers import routers_list
import settings

updater = Updater(settings.token)


def run_bot():
    for r in routers_list:
        updater.dispatcher.add_handler(r)
    updater.start_polling()


def send_tags_message(tag, message):
    chats = []
    if isinstance(tag, int):
        chats = controllers.get_chats_tag(tag)
    elif isinstance(tag, str):
        tags = controllers.get_tags()
        for t in tags:
            if t.name == tag:
                chats = controllers.get_chats_tag(t.id)
                break
        else:
            return

    views.send_message(message, chats, updater.dispatcher.bot)

