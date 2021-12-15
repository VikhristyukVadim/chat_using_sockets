from main_socket_file import Socket
import asyncio
from datetime import datetime
from os import system


class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()

        self.messages = ""

    def set_up(self):
        try:
            self.socket.connect(('127.0.0.1', 55555))
        except ConnectionRefusedError or ConnectionError:
            print("Server is offline")
            exit(0)

        self.socket.setblocking(False)

    async def listen_socket(self, listened_socket=None):
        while True:
            data = await self.main_loop.sock_recv(self.socket, 1024)
            self.messages += f"{datetime.now().date()} [{datetime.now().strftime('%H:%M:%S')}] ->" \
                             f" {data.decode('utf-8')} \n"

            system("clear")
            print(self.messages)

    async def send_data(self, data=None):
        while True:
            data = await self.main_loop.run_in_executor(None, input)
            await self.main_loop.sock_sendall(self.socket, data.encode('utf-8'))

    async def main(self):
        listening_task = self.main_loop.create_task(self.listen_socket())
        sending_task = self.main_loop.create_task(self.send_data())
        #
        # await asyncio.gather(
        #     self.main_loop.create_task(self.listen_socket()),
        #     self.main_loop.create_task(self.send_data())
        # )
        return await asyncio.gather(listening_task, sending_task, return_exceptions=True)


if __name__ == '__main__':
    client = Client()
    client.set_up()

    client.start()
