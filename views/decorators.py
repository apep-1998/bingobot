from controllers import controllers
from telegram import Update
import settings


def admin_required(function):
    def inner_function(update: Update, context):
        user_id = update.message.from_user.id
        if controllers.is_admin(user_id):
            function(update, context)
        else:
            update.message.reply_text(settings.admin_required)

    return inner_function


def add_user_chat(function):
    def inner_function(update: Update, context):
        controllers.add_user(
            telegram_id=update.message.from_user.id,
            fname=update.message.from_user.first_name,
            lname=update.message.from_user.last_name,
            username=update.message.from_user.username,
            is_bot=update.message.from_user.is_bot
        )

        chat = update.message.chat
        if chat.type == "private":
            title = update.message.from_user.full_name
        else:
            title = chat.title

        controllers.add_chat(chat_id=chat.id,
                             title=title,
                             _type=chat.type)

        function(update, context)

    return inner_function
