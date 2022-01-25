from pony.orm import *

db = Database('sqlite', 'my_db.sqlite', create_db=True)


# Create data base entity____   _______________________________________________________________________________________
class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    login = Required(str, unique=True)
    password = Required(str)
    message = Set(lambda: Messages, reverse='user')


class Messages(db.Entity):
    id = PrimaryKey(int, auto=True)
    user = Optional(User, reverse='message')
    record = Required(str)
    room = Optional(str, unique=True)


@db_session
def insert_message(message_txt, user_login):
    find_user = User.select(lambda user: user_login in user.login).get().id
    if User[find_user]:
        Messages(record=message_txt, user=find_user)
        commit()


@db_session
def create_user(new_name, new_pass):
    new_user = User(login=new_name, password=new_pass)
    commit()
    return new_user.login


@db_session
def check_user(user_login):
    users = User.get(login=user_login)
    if users:
        return True
    else:
        return False


@db_session
def check_user_in(user_login, password):
    users = User.get(login=user_login, password=password)
    if users:
        return True
    else:
        return False


db.generate_mapping(create_tables=True)
