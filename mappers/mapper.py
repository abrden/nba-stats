from multiprocessing import Process
import logging
import random

import zmq


class Mapper(Process):

    class MapperMiddleware:
        def __init__(self, mw_endpoint, key_queue_endpoint):
            context = zmq.Context()

            self.mw_socket = context.socket(zmq.REQ)
            self.mw_socket.setsockopt(zmq.REQ_RELAXED, 1)
            self.mw_socket.setsockopt(zmq.REQ_CORRELATE, 1)
            self.mw_socket.connect(mw_endpoint)

            self.key_queue_socket = context.socket(zmq.PUSH)
            self.key_queue_socket.connect(key_queue_endpoint)

        def send(self, data):
            return self.mw_socket.send(data)

        def notify_key(self, key):
            return self.key_queue_socket.send(key)

    def __init__(self, mw_endpoint, key_queue_endpoint, data):
        super().__init__()
        self.logger = logging.getLogger("Mapper")
        self.mw_endpoint = mw_endpoint
        self.key_queue_endpoint = key_queue_endpoint
        self.data = data
        self.mw = None

    def run(self):
        self.mw = self.MapperMiddleware(self.mw_endpoint, self.key_queue_endpoint)  # FIXME doesnt work if I initialize it on the constructor

        self.logger.debug("Working with data: %s", self.data)
        for i in self.data:
            key = random.choice([b'A', b'B'])
            value = "hello world {}".format(i).encode()
            self.logger.debug("Emitting result: (%s, %s)", key, value)
            self.mw.notify_key(key)
            self.mw.send(key + "#".encode() + value)
        self.mw.send(b'END')
