from main_socket_file import Socket
from threading import Thread


class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()

        self.listen(10)
        print('Server is running, please, press ctrl+c to stop')
        self.users = []

    def set_up(self):
        self.bind(('', 55555))
        self.accept_sockets()

    def send_data(self, data):
        for user in self.users:
            user.send(data)

    def listen_socket(self, listened_socket=None):
        print("listening user")
        while True:
            data = listened_socket.recv(1024)
            print(f'user send {str(data)}')

            self.send_data(data)

    def accept_sockets(self):
        while True:
            user_socket, addr = self.accept()
            print(f'User < {addr[0]} > connected', )

            self.users.append(user_socket)

            listen_accepted_user = Thread(target=self.listen_socket, args=(user_socket,))

            listen_accepted_user.start()


if __name__ == '__main__':
    server = Server()
    server.set_up()
