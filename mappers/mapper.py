from multiprocessing import Process
import logging

import zmq


class Mapper(Process):

    class MapperMiddleware:
        def __init__(self, endpoint):
            context = zmq.Context()
            self.socket = context.socket(zmq.REQ)
            self.socket.setsockopt(zmq.REQ_RELAXED, 1)
            self.socket.setsockopt(zmq.REQ_CORRELATE, 1)
            self.socket.connect(endpoint)

        def send(self, data):
            return self.socket.send(data)

    def __init__(self, endpoint, data):
        super().__init__()
        self.logger = logging.getLogger("Mapper")
        self.endpoint = endpoint
        self.data = data
        self.mw = None

    def run(self):
        self.mw = self.MapperMiddleware(self.endpoint)  # FIXME doesnt work if I initialize it on the constructor

        self.logger.debug("Working with data: %s", self.data)
        for i in self.data:
            result = "hello world {}".format(i)
            self.logger.debug("Emitting result: %s", result)
            self.mw.send(result.encode())
        self.mw.send(b'END')
