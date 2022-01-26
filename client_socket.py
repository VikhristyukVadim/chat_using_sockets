import socket

from methods import PostCommands
import re
from termcolor import colored
from threading import Thread
import datetime

from read_line import input_ing
from server_socket import add_new_user

date_now = datetime.datetime.now()
command = PostCommands()


class Client(socket.socket):
    """
        Client socket class, make client entity
    """
    def __init__(self, argument_parser, arg_values):
        super(Client, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.arg_values = arg_values
        self.client_argument_parser = argument_parser

        self.login = ""
        self.messages = ""
        self.chat_room = False

    def set_up(self):
        """
            Let's start listening to threads
        """
        try:
            listen_thread = Thread(target=self.listen_socket)
            listen_thread.start()

            send_thread = Thread(target=self.send_data)
            send_thread.start()

        except ConnectionRefusedError:
            print("Server is offline")
            exit(0)
        except BrokenPipeError as err:
            print(err)

    def listen_socket(self):
        """
            Listening to streams, processing server response options
        """
        try:
            while True:
                data = self.recv(2048)
                res_data = re.search(r'(.*)::(.*)::(.*)', data.decode("utf-8"))
                user_login = None
                server_command = None
                server_command_value = None
                if res_data:
                    user_login = res_data.group(1)
                    server_command = res_data.group(2)
                    server_command_value = res_data.group(3)

                if not data:
                    exit(0)
                elif data.decode('utf-8') == "USER_NOT_FOUND":
                    print(colored("This user is not registered ", "red"))
                    self.close()

                elif data.decode('utf-8') == "USER_WAS_FOUND":
                    res = colored("You are entered", 'green')
                    help_info = colored(" use HELP for usage information","yellow")
                    print(res + help_info)
                    self.set_up()
                elif server_command == "INVITE":
                    print(colored(user_login, "red") + server_command_value +
                          f'{colored(" are you agree to connect?", "yellow")}{colored(" YES|NO:", "green")}')
                    self.send_data()
                elif res_data:
                    if server_command == "PM":
                        print(colored(user_login, 'blue') + colored(" send to you: ", 'yellow') +
                              colored(server_command_value, "red"))

                else:
                    res_data = data.decode("utf-8")
                    self.messages += f'{res_data}\n'

                    print(res_data)
        except OSError or ValueError as err:
            print(err)
            exit(0)

    def send_login_data(self, login_data=None):
        """
        Sending a login request
        :param login_data:(str)
        """
        send_data = command.ASEND + "::" + login_data
        try:
            self.send(send_data.encode("utf-8"))
        except ConnectionError as err:
            print("error:", err)
        except OSError as e:
            print("error:", e)
            self.close()
            self.logining()

    def send_data(self):
        """
            process query variants and form a string for transmission to the server
        """
        try:
            while True:
                user_input = input_ing()
                try:
                    if user_input == 'CREATE_ROOM':
                        create_new_room = self.login + "::" + command.SUBSCRIBE + "::" + input_ing('input room name: ')
                        self.send(create_new_room.encode("utf-8"))
                    elif user_input == "OUT":
                        print(colored("you are out of the app ", 'yellow'))
                        self.shutdown(2)
                        self.close()
                    elif user_input == "LEAVE_ROOM":
                        input_user_name = self.login + "::" + command.UNSUBSCRIBE + "::" + self.login
                        self.send(input_user_name.encode("utf-8"))
                    elif user_input == "JOIN_ROOM":
                        selected_room = self.login + "::" + command.JOIN + "::" + input_ing("input room name: ")
                        self.send(selected_room.encode("utf-8"))
                    elif user_input == "INVITE_USER":
                        input_user_name = self.login + "::" + command.INVITE + "::" + input_ing("input name: ")
                        self.send(input_user_name.encode("utf-8"))
                    elif user_input == "DELETE_USER":
                        input_user_name = self.login + "::" + command.DELETE_USER + "::" + input_ing("input name: ")
                        self.send(input_user_name.encode("utf-8"))
                    elif user_input == "ROOM_LIST":
                        look_for_the_rooms = self.login + "::" + command.ROOMS + "::" + self.login
                        self.send(look_for_the_rooms.encode("utf-8"))
                    elif user_input == "USERS_LIST":
                        look_for_the_users = self.login + "::" + command.USERS + "::" + self.login
                        self.send(look_for_the_users.encode("utf-8"))
                    elif user_input == 'HELP':
                        show_app_commands = self.login + "::" + command.HELP + "::" + self.login
                        self.send(show_app_commands.encode("utf-8"))
                    elif user_input == "YES":
                        input_user_name = self.login + "::" + command.AGREE + "::" + user_input
                        self.send(input_user_name.encode("utf-8"))
                    elif user_input == "SEND_TO":
                        input_user_name = self.login + "::" + command.PM + "::" + input_ing(
                            'user name: ') + '::' + input('text: ')
                        self.send(input_user_name.encode("utf-8"))

                    else:
                        input_data = self.login + "::" + "MESSAGE" + "::" + user_input
                        self.send(input_data.encode("utf-8"))

                except Exception as err:
                    print(err)
        except ValueError as err:
            print(err)

    def logining(self):
        """
            login form
        """
        try:
            self.connect((self.arg_values.ip, int(self.arg_values.port)))
            if self.arg_values.r:
                self.reg()
            else:
                print("Enter login:")
                log = input_ing()
                print("Enter password:")
                pas = input()

                send_logining_data = (log + "  " + pas)
                self.login = log
                self.send_login_data(send_logining_data)
                self.listen_socket()
        except ConnectionRefusedError as err:
            print(err)

    def reg(self):
        """
            registration form
        """

        print("Register please")
        new_user_login = input("Login: ")
        new_user_password = input("Password: ")

        add_user = add_new_user(new_user_login, new_user_password)

        if add_user is not None:
            print(f"You are logged in as {new_user_login}")
            user = Client(self.client_argument_parser, self.client_argument_parser())
            user.login = new_user_login
            user.set_up()
        else:
            print(" This name already exists ")
            self.reg()
