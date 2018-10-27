from multiprocessing import Process
import logging

import zmq


class Reducer(Process):

    class ReducerMiddleware:
        def __init__(self, key, endpoint, reducer_ready_endpoint):
            context = zmq.Context()
            self.s = context.socket(zmq.DEALER)
            self.s.setsockopt(zmq.IDENTITY, key)
            self.s.connect(endpoint)

            reducer_ready_ack = context.socket(zmq.PUSH)
            reducer_ready_ack.connect(reducer_ready_endpoint)
            reducer_ready_ack.send(key)

        def receive(self):
            return self.s.recv()

    def __init__(self, key, endpoint, reducer_ready_endpoint):
        super().__init__()
        self.logger = logging.getLogger("Reducer-%s" % key)
        self.key = key
        self.endpoint = endpoint
        self.reducer_ready_endpoint = reducer_ready_endpoint
        self.mw = None

    def run(self):
        self.mw = self.ReducerMiddleware(self.key, self.endpoint, self.reducer_ready_endpoint)  # FIXME doesnt work if I initialize it on the constructor

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
