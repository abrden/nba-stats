from multiprocessing import Process
import logging

import zmq


class Reducer(Process):

    class ReducerMiddleware:
        def __init__(self, key, endpoint, context=None):
            context = context or zmq.Context()
            self.s = context.socket(zmq.DEALER)
            self.s.setsockopt(zmq.IDENTITY, key)
            self.s.connect(endpoint)

        def receive(self):
            return self.s.recv()

    def __init__(self, key, endpoint, context=None):
        super().__init__()
        self.logger = logging.getLogger("Reducer-%s" % key)
        self.key = key
        self.endpoint = endpoint
        self.context = context
        self.mw = None

    def run(self):
        self.mw = self.ReducerMiddleware(self.key, self.endpoint, self.context)  # FIXME doesnt work if I initialize it on the constructor

        self.logger.debug("Running")
        total = 0
        while True:
            # We receive one part, with the workload
            self.logger.debug("Receiving")
            request = self.mw.receive()
            self.logger.debug("Received msg: %r", request)
            finished = request == b"END"
            if finished:
                self.logger.debug("%s received: %s", self.key, total)
                break
            self.logger.debug("Adding up")
            total += 1
