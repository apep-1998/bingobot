from model import models
from sqlalchemy.orm import sessionmaker

__Session = sessionmaker(bind=models.engine)


def is_admin(telegram_id):
    try:
        session = __Session()
        user = session.query(models.User).get(telegram_id)
        return user.is_admin
    except Exception as e:
        print(e)
        return False


def make_admin(telegram_id):
    session = __Session()
    user = session.query(models.User).get(telegram_id)
    user.is_admin = True
    session.add(user)
    session.commit()
    session.close()


def add_user(telegram_id, fname='', lname='', username='', is_bot=False):
    try:
        session = __Session()
        user = models.User(telegram_id=telegram_id,
                           first_name=fname,
                           last_name=lname,
                           username=username,
                           is_bot=is_bot)
        session.add(user)
        session.commit()
        session.close()
    except Exception as e:
        pass


def add_chat(chat_id, title='', _type=''):
    try:
        session = __Session()
        chat = models.Chat(chat_id=chat_id,
                           title=title,
                           type=_type)
        session.add(chat)
        session.commit()
        session.close()
    except Exception as e:
        pass


def commit_query(*args):
    session = __Session()
    for arg in args:
        session.add(arg)
    session.commit()
    session.close()


def add_new_tag(name, description=''):
    try:
        session = __Session()
        tag = models.Tag(name=name, description=description)
        session.add(tag)
        session.commit()
        session.close()
        return {"status": "ok"}
    except Exception as e:
        return {
            'status': 'fail',
            'message': str(e)
        }


def remove_tag(pk):
    try:
        session = __Session()
        tag = session.query(models.Tag).get(pk)
        session.delete(tag)
        session.commit()
        session.close()
        return {"status": "ok"}
    except Exception as e:
        return {
            'status': 'fail',
            'message': str(e)
        }


def get_tags():
    session = __Session()
    tags = session.query(models.Tag).all()
    session.close()
    return tags


def get_users():
    session = __Session()
    users = session.query(models.User).all()
    session.close()
    return users


def get_chats():
    session = __Session()
    chats = session.query(models.Chat).all()
    session.close()
    return chats


def add_chat_to_tag(chat_id, tag_id):
    session = __Session()
    try:
        chat = session.query(models.Chat).get(chat_id)
        tag = session.query(models.Tag).get(tag_id)
        tag.chats.append(chat)
        session.add(tag)
        session.commit()
        session.close()
    except Exception as e:
        print(e)


def remove_chat_from_tag(chat_id, tag_id):
    session = __Session()
    try:
        chat = session.query(models.Chat).get(chat_id)
        tag = session.query(models.Tag).get(tag_id)
        tag.chats.remove(chat)
        session.add(tag)
        session.commit()
        session.close()
    except Exception as e:
        print(e)


def get_tags_chat(chat_id):
    session = __Session()
    chat_tags = session.query(models.association_table).filter(models.association_table.c.chats_id == chat_id).all()
    session.close()
    return [item[1] for item in chat_tags]


def get_chats_tag(tag_id):
    session = __Session()
    tag_list = session.query(models.association_table).filter(models.association_table.c.tags_id == tag_id).all()
    session.close()
    return [item[0] for item in tag_list]
