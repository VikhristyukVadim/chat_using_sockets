import socket
import re

from pony import orm
import datetime
from termcolor import colored

from Pony_file import insert_message, check_user, create_user, check_user_in
from threading import Thread

from methods import PostCommands, show_help_command

date_now = datetime.datetime
command = PostCommands()


class UserEntity:
    """
    user entity class
    """

    def __init__(self, name, socket_address, object_socket):
        self.name = name,
        self.socket_address = socket_address,
        self.object_socket = object_socket


class RoomEntity:
    """
    room entity class
    """

    def __init__(self, name):
        self.name = name
        self.guests = []

    def addition_user(self, user):
        """
        Adding a new user
        :param user: user login
        """
        self.guests.append(user)

    def removing_user(self, user):
        """
        remove user
        :param user: user login
        """
        self.guests.remove(user)

    def change_room_name(self, new_name):
        """
        new name for the room
        """
        self.name = new_name


def user_logining(listened_socket):
    """
    login
    :param listened_socket: user socket
    :return:
    """
    data = listened_socket.recv(2048)
    logining_data = re.search(r'(.*)::(.*)\s\s(.*)', data.decode('utf-8'))

    check = user_checking(logining_data.group(2), logining_data.group(3))

    if logining_data and check:
        if check_user_in(logining_data.group(2), logining_data.group(3)):
            return str(logining_data.group(2))
        else:
            return False
    else:
        pass


class Server(socket.socket):
    """
    server socket class
    """

    def __init__(self):
        super(Server, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        print('Server is running, please, press ctrl+c to stop')
        self.users = []
        self.rooms = []
        self.inviting = None

    def set_up(self):
        """
        socket connection
        """
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind(('', 55555))
        self.listen(10)
        self.accept_sockets()

    def check_for_presence_in_the_room(self, user):
        """
        checking if a user is in the room
        :param user: str
        :return: room
        """
        for room in self.rooms:
            for guest in room.guests:
                if user == "".join(guest.name):
                    return room
                else:
                    pass

    def find_user_by_name(self, user_login):
        """
        checking if a user is in the user list
        :param user_login: str
        :return: user
        """
        for user in self.users:
            if user_login == "".join(user.name):
                return user

    def send_data(self, data, message_author):
        """
        sending information to the client
        :param data: sending data
        :param message_author: message author
        """
        try:
            room_guests_list = self.check_for_presence_in_the_room(message_author)
            if room_guests_list and type(room_guests_list.guests) is list:
                for i in room_guests_list.guests:
                    i.object_socket.send(data.encode('utf-8'))
            else:
                for user in self.users:
                    user.object_socket.send(data.encode('utf-8'))
        except OSError as err:
            print(err)

    def login_error_data(self, data, user_socket):
        """
        connection error handling
        :param data: str
        :param user_socket: socket
        """
        user_socket.send(data.encode('utf-8'))

        print(f"Client {user_socket.getpeername()[1]} removed")

        user_socket.close()
        self.accept_sockets()

    def delete_log_out_user(self, listened_socket):
        """
        remove a logged out user from the list
        :param listened_socket: socket
        """
        for key, i in enumerate(self.users):
            if i.object_socket == listened_socket:
                del self.users[key]

    def listen_socket(self, listened_socket=None):
        """
        listening to clients
        :param listened_socket: socket
        """
        while True:
            try:
                # get the date and time to identify the message
                sending_date = f'{date_now.now().strftime("%d-%m-%Y")}'
                sending_time = f' [{date_now.now().strftime("%H:%M:%S") + "]"}'

                # listening on a socket
                data = listened_socket.recv(2048)

                if not data:
                    # checking if the client has crashed
                    print(f"Client {listened_socket.getpeername()[1]} removed")
                    self.delete_log_out_user(listened_socket)
                    listened_socket.close()
                    break

                # information decoding
                sending_data = data.decode("utf-8")

                # split the string
                res_data = re.search(r'(.*)::(.*)::(.*)::(.*)', sending_data) or re.search(r'(.*)::(.*)::(.*)',
                                                                                           sending_data)
                if res_data:
                    user_login = res_data.group(1)
                    user_command = res_data.group(2)
                    user_command_value = res_data.group(3)

                    if user_command == "MESSAGE":
                        if user_command_value:
                            presence = self.check_for_presence_in_the_room(user_login)
                            room_name = f'{colored(" send to the chat", "yellow", attrs=["dark"])}' \
                                        f' {"(" + colored(presence.name, "green") + "): "}' if presence is not None else " send: "

                            insert_message(user_command_value, user_login)

                            sending_data = f'{colored(sending_date + sending_time + ">>> ", "cyan")}' \
                                           f'{colored(user_login, "green", attrs=["bold"])}' + \
                                           colored(room_name, "yellow") + colored(user_command_value, "white")

                            self.send_data(sending_data, user_login)
                        else:
                            pass

                    elif user_command == "PM":
                        res_data = re.search(r'(.*)::(.*)::(.*)::(.*)', sending_data)

                        private_message_text = res_data.group(4)
                        addressed_user = self.find_user_by_name(user_command_value)
                        if "".join(addressed_user.name) == user_login:
                            message = colored("No need to send messages to yourself, send to someone else :) ",
                                              'yellow')
                            addressed_user.object_socket.send(message.encode('utf-8'))
                        else:
                            message = colored(sending_date + sending_time + '>>> ',
                                              'cyan') + user_login + "::" + "PM" + "::" + private_message_text
                            addressed_user.object_socket.send(message.encode('utf-8'))

                    elif user_command == "SUBSCRIBE":
                        new_room = RoomEntity(user_command_value)
                        for user in self.users:
                            if "".join(user.name) == user_login:
                                new_room.addition_user(user)
                                self.rooms.append(new_room)
                                self.send_data(colored(user_login, 'cyan') +
                                               colored(" joined to the chat room: ", "yellow") +
                                               colored(user_command_value, 'cyan'), user_login)

                    elif user_command == "JOIN":
                        found_room = self.check_for_presence_in_the_room(user_login)
                        user = self.find_user_by_name(user_login)
                        if found_room and found_room.guests is None:
                            for i in self.rooms:
                                if i.name == user_command_value:
                                    i.guests.append(user)
                                    info_message = colored(sending_date + sending_time + '>>> ', 'cyan') + \
                                                   f"{colored(user_login, 'cyan')} " \
                                                   f"{colored('joined to the chat room:', 'yellow')}" \
                                                   f" ({colored(user_command_value, 'green')})"
                                    self.send_data(info_message, user_login)
                        else:
                            if found_room:
                                found_room.guests.remove(user)
                            for i in self.rooms:
                                if i.name == user_command_value:
                                    i.guests.append(user)
                                    info_message = colored(sending_date + sending_time + '>>> ', 'cyan') + \
                                                   f"{colored(user_login, 'cyan')} " \
                                                   f"{colored('joined to the chat room:', 'yellow')}" \
                                                   f" ({colored(user_command_value, 'green')})"
                                    self.send_data(info_message, user_login)

                    elif user_command == 'INVITE' and check_user(user_command_value):
                        invited_user = self.find_user_by_name(user_command_value)
                        invitation = colored(sending_date + sending_time + '>>> ', 'cyan') + \
                                     user_login + "::" + "INVITE" + "::" + " invite you to the chat"
                        invited_user.object_socket.send(invitation.encode('utf-8'))
                        self.inviting = user_login

                    elif user_command == "AGREE":
                        if len(self.rooms) == 0:
                            for user in self.users:
                                new_room = RoomEntity(user_login + "'s room")
                                if "".join(user.name) == user_login:
                                    new_room.addition_user(user)
                                if "".join(user.name) == user_command_value:
                                    new_room.addition_user(user_command_value)
                        else:
                            for room in self.rooms:
                                for user in self.users:
                                    if self.inviting == "".join(user.name):
                                        new_user = self.find_user_by_name(user_login)
                                        room.addition_user(new_user)
                                        room_to_join = self.check_for_presence_in_the_room(user_login)
                                        self.send_data(f"{colored(sending_date + sending_time + '>>> ', 'cyan')}"
                                                       f"{colored(user_login, 'cyan')}"
                                                       f"{colored(' join to the chat room', 'yellow')} ("
                                                       f"{colored(room_to_join.name, 'cyan')})", user_login)
                                        break

                    elif user_command == 'DELETE_USER' or user_command == 'UNSUBSCRIBE' and check_user(
                            user_command_value):
                        room_guests_list = self.check_for_presence_in_the_room(user_login)
                        deleted_user = self.find_user_by_name(user_login)
                        if room_guests_list and type(room_guests_list.guests) is list:
                            room_to_out = self.check_for_presence_in_the_room(user_login)
                            room_guests_list.guests.remove(deleted_user)
                            info_message = f"{colored(user_login, 'cyan')} " \
                                           f"{colored('left the chat room ', 'yellow') + '(' + colored(room_to_out.name, 'green') + ')'}"
                            self.send_data(info_message, user_login)

                    elif user_command == "ROOMS":
                        room_list = ""
                        if len(self.rooms) == 0:
                            room_list = "There are no rooms "
                        else:
                            room_list = "room list: "
                            for i in self.rooms:
                                room_list += i.name + " "
                        listened_socket.send(room_list.encode('utf-8'))
                    elif user_command == "USERS":
                        users_list = ""
                        if len(self.users) == 0:
                            users_list = "There are no users "
                        else:
                            users_list = colored("users_list (" + str(len(self.users)) + "): ", 'yellow')
                            for i in self.users:
                                users_list += ''.join(i.name) + ", "
                        listened_socket.send(users_list.encode('utf-8'))

                    elif user_command == "HELP":
                        commands = show_help_command()
                        help_command_list = ""
                        for item in commands:
                            line = colored(item, 'yellow') + " : " + colored(str(commands.get(item)), 'green') + '\n'
                            help_command_list += line

                        listened_socket.send(help_command_list.encode('utf-8'))
                    else:
                        self.send_data("USER NOT FOUND", user_login)
                    pass

            except ConnectionResetError or OSError:
                self.delete_log_out_user(listened_socket)
                return

    def accept_sockets(self):
        """
        Analysis of information about the logged in user
        """
        try:
            while True:
                user_socket, addr = self.accept()
                print(f'User < {addr[1]} {addr[0]} > connected', )

                registered_user = user_logining(user_socket)
                present_user = self.find_user_by_name(registered_user)

                if registered_user:
                    if present_user and "".join(present_user.name) == registered_user:
                        new_data = colored("A user with the same name is already online.", "red")
                        self.login_error_data(new_data, user_socket)
                    else:
                        user_socket.send("USER_WAS_FOUND".encode('utf-8'))
                        new_user = UserEntity(registered_user, addr[1], user_socket)
                        self.users.append(new_user)
                        listen_accepted_user = Thread(target=self.listen_socket, args=(user_socket,))
                        listen_accepted_user.start()
                else:
                    new_data = "USER_NOT_FOUND"
                    self.login_error_data(new_data, user_socket)
        except KeyError as err:
            print(err)
        except EOFError as err:
            print(err)
        except KeyboardInterrupt as err:
            print(err)
        except OSError as err:
            print(err)


def user_checking(login, password):
    """
    check the database for the existence of such a user
    :param login: any
    :param password: any
    :return:
    """
    return check_user_in(login, password)


def add_new_user(login, password):
    """
    create new user in db
    :param login: any
    :param password: any
    :return: new user login
    """
    try:
        return create_user(login, password)
    except Exception as err:
        print('Exception error: ', err)


def add_new_message(user, message):
    """
    crate new message in db
    :param user: author
    :param message: text
    """
    try:
        return insert_message(message, user)
    except orm.core.ObjectNotFound:
        print('orm.core.ObjectNotFound', orm.core.ObjectNotFound, orm.core.OrmError.args)
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


if __name__ == '__main__':
    server = Server()
    server.set_up()
