from views import views
from telegram.ext import CommandHandler, CallbackQueryHandler


routers_list = [
    CommandHandler('start', views.start_view),
    CommandHandler('addtag', views.add_new_tag_view, pass_args=True),
    CommandHandler('tags', views.tags_list_view),
    CommandHandler('users', views.users_list_view),
    CommandHandler('chats', views.chats_list_view),
    CommandHandler('rmtag', views.remove_tag_view, pass_args=True),
    CommandHandler('admin', views.make_user_admin_view, pass_args=True),
    CommandHandler('sendall', views.send_all_view, pass_args=True),
    CommandHandler('sendtag', views.send_tag_message, pass_args=True),

    CommandHandler('tagselect', views.select_tags_list),
    CallbackQueryHandler(views.callbackQuery)
]
