import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.absolute()

##################################################################
# Bot settings
##################################################################
token = '<bot-token>'
password = '<bot-password>'
# if set this flag false user can't select tags
tag_public = True

##################################################################
# database setting
##################################################################
database_address = os.path.join(BASE_DIR, 'database.db')

##################################################################
# text message
##################################################################
admin_required = "this command admin required"
admin_menu = """
/addtag <name> <description:!> - to add new tag
/rmtag <tag pk> - remove tag
/admin <password> - make admin
/tags - list of tags
/users - list of users
/chats - list of chats
/sendtag <tag_id> <message> - send tag msessage <
/sendall - send message for all chats
"""
