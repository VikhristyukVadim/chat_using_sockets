from main_socket_file import Socket
import asyncio
import socket


class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()

        self.users = []

    def set_up(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('127.0.0.1', 55555))
        self.socket.listen(10)
        print('Server is running, please, press ctrl+c to stop')
        self.socket.setblocking(False)

    async def send_data(self, data):
        for user in self.users:
            await self.main_loop.sock_sendall(user, data)

    async def listen_socket(self, listened_socket=None):

        if not listened_socket:
            return

        while True:

            data = await self.main_loop.sock_recv(listened_socket, 1024)

            await self.send_data(data)
            # try:
            #     print("listening user", listened_socket)
            #     data = await self.main_loop.sock_recv(listened_socket, 1024)
            #
            #     # print(f'user send {str(data).encode("utf-8")}')
            #     await self.send_data(data)
            # except ConnectionResetError:
            #     print("Client removed")
            #     self.users.remove(listened_socket)
            #     return

    async def accept_sockets(self):
        while True:
            user_socket, addr = await self.main_loop.sock_accept(self.socket)
            print(f'User < {addr[0]} > connected')

            self.users.append(user_socket)
            self.main_loop.create_task(self.listen_socket(user_socket))

    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())


if __name__ == '__main__':
    server = Server()
    server.set_up()

    server.start()
