from multiprocessing import Process
import logging
import pickle

import zmq


class Reducer(Process):

    class MiddlewareConnection:
        def __init__(self, key, endpoint, reducer_ready_endpoint):
            context = zmq.Context()
            self.s = context.socket(zmq.DEALER)
            self.s.setsockopt(zmq.IDENTITY, key)
            self.s.connect(endpoint)

            reducer_ready_ack = context.socket(zmq.PUSH)
            reducer_ready_ack.connect(reducer_ready_endpoint)
            reducer_ready_ack.send(key)

        def receive(self):
            b_data = self.s.recv()
            return pickle.loads(b_data)


    class SinkConnection:
        def __init__(self, key, endpoint):
            self.key = key.decode()

            context = zmq.Context()

            self.client = context.socket(zmq.PUSH)
            self.client.connect(endpoint)

        def send_result(self, result):
            self.client.send_string(self.key + "#" + str(result))

    def __init__(self, key, endpoint, reducer_ready_endpoint, sink_endpoint, fun):
        super().__init__()
        self.logger = logging.getLogger("Reducer-%s" % key)
        self.key = key
        self.endpoint = endpoint
        self.reducer_ready_endpoint = reducer_ready_endpoint
        self.sink_endpoint = sink_endpoint
        self.fun = fun
        self.mw = None
        self.sink_conn = None

    def run(self):
        self.mw = self.MiddlewareConnection(self.key, self.endpoint, self.reducer_ready_endpoint)  # FIXME doesnt work if I initialize it on the constructor
        self.sink_conn = self.SinkConnection(self.key, self.sink_endpoint)

        self.logger.debug("Running")
        acc = None
        while True:
            # We receive one part, with the workload
            self.logger.debug("Receiving")
            request = self.mw.receive()
            self.logger.debug("Received msg: %r", request)
            finished = request == "END"
            if finished:
                self.logger.debug("%s received: %s", self.key, acc)
                break

            self.logger.debug("Processing task")
            acc = self.fun(acc, request)

        self.logger.debug("Sending final result %r to sink", acc)
        self.sink_conn.send_result(acc)

        import time
        time.sleep(1)  # FIXME Wait for sink to read it before exiting
