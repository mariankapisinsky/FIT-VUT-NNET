#!/usr/bin/python3

import asyncio
import logging
import socket

class Wrapper():
    def __init__(self, wrapped):
        self._wrapped = wrapped
    def __getattr__(self, name):
        # https://docs.python.org/3/reference/datamodel.html#object.__getattr__
        return getattr(self._wrapped, name)

class ListeningSocket(Wrapper):
    def __init__(self, local_port, loop):
        Wrapper.__init__(self, socket.socket())
        self._wrapped.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._wrapped.bind(("0.0.0.0", int(local_port)))
        self._wrapped.setblocking(False) # otherwise ValueError: the socket must be non-blocking
        self._loop = loop

    async def accept_connection(self):
        logging.debug("Awaiting connection")
        connection, address = await self._loop.sock_accept(self._wrapped)
        logging.debug("Connection received from %s" % str(address))
        wrapped_connection = ProcessingSocket(connection, self._loop)
        self._loop.create_task(self.accept_connection())
        await self._loop.create_task(wrapped_connection.do_work())

class ProcessingSocket(Wrapper):
    def __init__(self, connection, loop):
        Wrapper.__init__(self, connection)
        self._client = connection
        self._client.setblocking(False) # With SelectorEventLoop event loop, the socket sock must be non-blocking.
        self._read_size = 2048
        self._loop = loop

    async def do_work(self):
        logging.debug("Waiting for data from client")
        while True:
            logging.debug("Waiting for %d bytes from %s" % (self._read_size, self._client.getpeername()))
            data = await self._loop.sock_recv(self._client, self._read_size)
            logging.debug("Received %d bytes from %s" % (len(data), self._client.getpeername()))
            if data:
                await self._loop.sock_sendall(self._client, data.swapcase())
                logging.debug("Data case-swapped and returned for %s" % str(self._client.getpeername()))
            else:
                self._client.close()
                break


def init(local_port):
    loop = asyncio.get_event_loop()
    listening = ListeningSocket(local_port, loop)
    listening.listen()
    loop.create_task(listening.accept_connection())
    loop.run_forever()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='An example of a Python async server for ISA.'
        )
    parser.add_argument("--port", "-p", type=int, required=True,
            help="Local port listening for clients")
    parser.add_argument("--verbosity", "-v",
            choices=["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL",  "FATAL"],
            default="WARN", help="Enable logging to stdout on given levels")
    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.verbosity))
    init(args.port)
