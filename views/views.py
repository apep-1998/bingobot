from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from controllers import controllers
from views import decorators
import settings
import time


def send_message(text, chats, bot):
    successful = 0
    unsuccessful = 0
    for chat in chats:
        for i in range(4):
            try:
                bot.sendMessage(chat, text)
                successful += 1
                break
            except Exception as e:
                time.sleep(3)
        else:
            unsuccessful += 1

    return successful, unsuccessful


@decorators.add_user_chat
def start_view(update: Update, context: CallbackContext):
    if context.chat_data.get('start', None) is not None:
        update.message.reply_text("to ghablan start kardi")
    else:
        update.message.reply_text("salam")
        context.chat_data["start"] = "salam in dadas!"


@decorators.admin_required
def add_new_tag_view(update: Update, context: CallbackContext):
    args = context.args
    if len(args) >= 1:
        name = ' '.join(args)
        result = controllers.add_new_tag(name=name)
        if result['status'] == 'ok':
            update.message.reply_text("tag added!")
        else:
            update.message.reply_text("error : {}".format(result['message']))
    else:
        update.message.reply_text("send args name description(optional)")


@decorators.admin_required
def tags_list_view(update: Update, context: CallbackContext):
    all_tags = controllers.get_tags()
    out_text = 'list of tags'
    keyboard = []
    for tag in all_tags:
        keyboard.append([InlineKeyboardButton(text='id', callback_data='1'),
                         InlineKeyboardButton(text=str(tag.id), callback_data='2')])
        keyboard.append([InlineKeyboardButton(text='name', callback_data='3'),
                         InlineKeyboardButton(text=tag.name, callback_data='4')])
        keyboard.append([InlineKeyboardButton(text='delete', callback_data='dt|{}'.format(tag.id))])
        keyboard.append([InlineKeyboardButton(text='==================', callback_data='split')])

    update.message.reply_text(out_text, reply_markup=InlineKeyboardMarkup(keyboard))


@decorators.admin_required
def users_list_view(update: Update, context: CallbackContext):
    all_users = controllers.get_users()
    out_text = 'list of users'
    keyboard = []
    for user in all_users:
        keyboard.append([InlineKeyboardButton(text='telegram id', callback_data='1')])
        keyboard.append([InlineKeyboardButton(text=str(user.telegram_id), callback_data='2')])
        if user.first_name:
            keyboard.append([InlineKeyboardButton(text='first name', callback_data='3'),
                             InlineKeyboardButton(text=user.first_name, callback_data='4')])
        if user.last_name:
            keyboard.append([InlineKeyboardButton(text='last name', callback_data='3'),
                             InlineKeyboardButton(text=user.last_name, callback_data='4')])
        if user.username:
            keyboard.append([InlineKeyboardButton(text='username', callback_data='3'),
                             InlineKeyboardButton(text=user.username, url='t.me/{}'.format(user.username))])
        keyboard.append([InlineKeyboardButton(text='==================', callback_data='split')])

    update.message.reply_text(out_text, reply_markup=InlineKeyboardMarkup(keyboard))


@decorators.admin_required
def chats_list_view(update: Update, context: CallbackContext):
    all_chats = controllers.get_chats()
    out_text = 'list of chat'
    keyboard = []
    for chat in all_chats:
        keyboard.append([InlineKeyboardButton(text='chat id', callback_data='1')])
        keyboard.append([InlineKeyboardButton(text=str(chat.chat_id), callback_data='2')])
        if chat.title:
            keyboard.append([InlineKeyboardButton(text='title', callback_data='3'),
                             InlineKeyboardButton(text=chat.title, callback_data='4')])
        keyboard.append([InlineKeyboardButton(text='type', callback_data='3'),
                         InlineKeyboardButton(text=chat.type, callback_data='4')])
        keyboard.append([InlineKeyboardButton(text='==================', callback_data='split')])

    update.message.reply_text(out_text, reply_markup=InlineKeyboardMarkup(keyboard))


@decorators.admin_required
def remove_tag_view(update: Update, context: CallbackContext):
    args = context.args
    if len(args) == 1:
        result = controllers.remove_tag(int(args[0]))
        if result['status'] == 'ok':
            update.message.reply_text('tag removed!')
        else:
            update.message.reply_text('error : {}'.format(result['message']))
    else:
        update.message.reply_text('use this command with tag id.')


@decorators.add_user_chat
def make_user_admin_view(update: Update, context: CallbackContext):
    args = context.args
    if len(args) == 1:
        if settings.password == args[0]:
            controllers.make_admin(update.message.from_user.id)
            update.message.reply_text('you are admin now!')
        else:
            update.message.reply_text('password incorrect!')
    else:
        update.message.reply_text(settings.admin_menu)


def get_chat_tag_keyboard(chat_id):
    keyboard = []
    chat_tags = controllers.get_tags_chat(chat_id)
    for tag in controllers.get_tags():
        if tag.id in chat_tags:
            keyboard.append(
                [InlineKeyboardButton(tag.name+"✅", callback_data=str('add2tag|{}'.format(tag.id)))]
            )
        else:
            keyboard.append(
                [InlineKeyboardButton(tag.name+"❌", callback_data=str('add2tag|{}'.format(tag.id)))]
            )

    return keyboard


@decorators.add_user_chat
def select_tags_list(update: Update, context: CallbackContext):
    if settings.tag_public:
        keyboard = InlineKeyboardMarkup(get_chat_tag_keyboard(update.message.chat_id))
        update.message.reply_text("this is list of tags", reply_markup=keyboard)
    else:
        update.message.reply_text("this bot is tag private")


@decorators.admin_required
def send_tag_message(update: Update, context: CallbackContext):
    tag_id = context.args[0]
    message = ' '.join(context.args[1:])
    if message:
        chats = controllers.get_chats_tag(tag_id)
        successful, unsuccessful = send_message(message, chats, context.dispatcher.bot)
        update.message.reply_text("""
📣📣 message sent 📣📣
✅ successful : {}
❌ unsuccessful : {} 
""".format(successful, unsuccessful))
    else:
        update.message.reply_text("user this command with a tag_id and message")


@decorators.admin_required
def send_all_view(update: Update, context: CallbackContext):
    message = ' '.join(context.args)
    if message:
        chats = [item.chat_id for item in controllers.get_chats()]
        successful, unsuccessful = send_message(message, chats, context.dispatcher.bot)
        update.message.reply_text("""
📣📣 message sent 📣📣
✅ successful : {}
❌ unsuccessful : {} 
""".format(successful, unsuccessful))
    else:
        update.message.reply_text("user this command with a message")


def callbackQuery(update: Update, context: CallbackContext):
    query = update.callback_query.data.split("|")
    command = query[0]
    chat_id = update.callback_query.message.chat_id
    if command == "add2tag":
        if int(query[1]) in controllers.get_tags_chat(chat_id):
            controllers.remove_chat_from_tag(chat_id, int(query[1]))
            update.callback_query.answer("you remove from this tag")
        else:
            controllers.add_chat_to_tag(chat_id, int(query[1]))
            update.callback_query.answer("you added to this tag")

        keyboard = InlineKeyboardMarkup(get_chat_tag_keyboard(chat_id))
        update.callback_query.message.edit_reply_markup(reply_markup=keyboard)

    elif command == 'dt':
        controllers.remove_tag(int(query[1]))
        all_tags = controllers.get_tags()
        keyboard = []
        for tag in all_tags:
            keyboard.append([InlineKeyboardButton(text='id', callback_data='1'),
                             InlineKeyboardButton(text=str(tag.id), callback_data='2')])
            keyboard.append([InlineKeyboardButton(text='name', callback_data='3'),
                             InlineKeyboardButton(text=tag.name, callback_data='4')])
            keyboard.append([InlineKeyboardButton(text='delete', callback_data='dt|{}'.format(tag.id))])
            keyboard.append([InlineKeyboardButton(text='==================', callback_data='split')])

        update.callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
        update.callback_query.answer("tag removed!")
