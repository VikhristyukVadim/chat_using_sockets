"""
ASEND: - authorisation
USER: - user login
PASS: - user password
STAT: - user status
DELETE: - delete message

SUBSCRIBE: - add user to the room
UNSUBSCRIBE: - remove user from the room

LIST: - list of available rooms
"""


class PostCommands:
    def __init__(self):
        self.PM = "PM"
        self.OUT = "OUT"
        self.PASS = "PASS"
        self.USER = "USER"
        self.STAT = "STAT"
        self.LIST = "LIST"
        self.JOIN = "JOIN"
        self.HELP = "HELP"
        self.ASEND = "ASEND"
        self.ROOMS = "ROOMS"
        self.USERS = "USERS"
        self.AGREE = "AGREE"
        self.INVITE = "INVITE"
        self.DELETE = "DELETE"
        self.SUBSCRIBE = "SUBSCRIBE"
        self.DELETE_USER = "DELETE_USER"
        self.UNSUBSCRIBE = "UNSUBSCRIBE"

    def checking_command(self, command, value=False):
        if command == self.ASEND:
            return "logining"
        if command == self.OUT:
            return "leave_application"
        if command == self.STAT:
            return "check_status"
        if command == self.DELETE:
            return "delete_message"

        if command == self.SUBSCRIBE:
            print('enter_to_the_room')
            return "enter_to_the_room"
        if command == self.UNSUBSCRIBE:
            print('leave_the_room')
            return "leave_the_room"
        if command == self.LIST:
            return "list_of_the_rooms"
        if command == self.INVITE:
            print('invite_to_the_room')
        if command == self.DELETE_USER:
            print('delete_user_from_room')
            return "delete_user_from_room"


command_list = {
    "request a list of commands": "..HELP",
    "list available users": "........USERS_LIST",
    "private message": ".............SEND_TO",
    "list available rooms": "........ROOM_LIST",
    "create new chat room": "........CREATE_ROOM",
    "leave chat room": ".............LEAVE_ROOM",
    "invite new user to chat room": "INVITE_USER",
    "remove user from chat room": "..DELETE_USER",
    "join an existing room": ".......JOIN_ROOM",
    "exit the application": "........OUT",





}


def show_help_command():
    return command_list
