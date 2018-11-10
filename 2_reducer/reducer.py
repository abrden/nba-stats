import logging
import pickle

import zmq


class Reducer:

    class MiddlewareConnection:
        def __init__(self, endpoint, reducer_ready_endpoint):
            self.endpoint = endpoint
            self.reducer_ready_endpoint = reducer_ready_endpoint
            self.sockets = {}
            self.poller = zmq.Poller()

        def register_key(self, key):
            context = zmq.Context()

            if key not in self.sockets:
                s = context.socket(zmq.DEALER)
                s.setsockopt(zmq.IDENTITY, key)
                s.connect(self.endpoint)
                self.sockets[s] = key
                self.poller.register(s, zmq.POLLIN)

        def signal_ready(self):
            context = zmq.Context()
            reducer_ready_ack = context.socket(zmq.PUSH)
            reducer_ready_ack.connect(self.reducer_ready_endpoint)
            reducer_ready_ack.send(b"READY")

        def receive(self):
            d = dict(self.poller.poll())
            pairs = []
            for s in d:
                if d[s] == zmq.POLLIN:
                    b_data = s.recv()
                    data = pickle.loads(b_data)
                    pairs.append((self.sockets[s], data))
            return pairs

    class ReducerHandlerConnection:
        def __init__(self, endpoint, reducer_ready_endpoint):
            context = zmq.Context()
            self.receiver = context.socket(zmq.PULL)
            self.receiver.connect(endpoint)

            reducer_ready_ack = context.socket(zmq.PUSH)
            reducer_ready_ack.connect(reducer_ready_endpoint)
            reducer_ready_ack.send(b"READY")

        def receive_key(self):
            return self.receiver.recv()

    class SinkConnection:
        def __init__(self, endpoint):
            context = zmq.Context()

            self.client = context.socket(zmq.PUSH)
            self.client.connect(endpoint)

        def send_result(self, result):
            for key in result:
                b_value = pickle.dumps((key.decode(), result[key]), -1)
                self.client.send(b_value)

    def __init__(self, endpoint, reducer_mw_ready_endpoint, keys_endpoint, reducer_handler_ready_endpoint, sink_endpoint):
        self.logger = logging.getLogger("Reducer")
        self.acc = {}
        self.endpoint = endpoint
        self.keys_endpoint = keys_endpoint
        self.reducer_mw_ready_endpoint = reducer_mw_ready_endpoint
        self.reducer_handler_ready_endpoint = reducer_handler_ready_endpoint
        self.sink_endpoint = sink_endpoint
        self.mw = None
        self.handler_conn = None
        self.sink_conn = None

    def start(self, fun):
        self.mw = self.MiddlewareConnection(self.endpoint, self.reducer_mw_ready_endpoint)  # FIXME doesnt work if I initialize it on the constructor
        self.handler_conn = self.ReducerHandlerConnection(self.keys_endpoint, self.reducer_handler_ready_endpoint)
        self.sink_conn = self.SinkConnection(self.sink_endpoint)

        acc = {}

        self.logger.debug("Receiving keys")
        while True:
            self.logger.debug("Receiving key from ReducerHandler")
            key = self.handler_conn.receive_key()
            if key == b'END':
                self.logger.debug("ReducerHandler END received")
                break
            self.logger.debug("Receiving key: %r", key)
            acc[key] = None
            self.mw.register_key(key)

        self.logger.debug("Signaling MW")
        self.mw.signal_ready()

        self.logger.debug("Working with values")
        ends_received = 0
        while True:
            self.logger.debug("Receiving")
            pairs = self.mw.receive()
            self.logger.debug("Received pairs: %r", pairs)

            end = False
            for request in pairs:
                finished = request[1] == "END"
                if finished:
                    self.logger.debug("MW END received")
                    ends_received += 1
                    if ends_received == len(acc):  # acc dict initializes with all the keys assigned to this reducer
                        end = True
                    continue

                key, value = request
                self.logger.debug("Processing task")
                acc[key] = fun(acc[key], value)

            if end:
                break

        self.logger.debug("Sending final result %r to sink", acc)
        self.sink_conn.send_result(acc)

        import time
        time.sleep(1)  # FIXME Wait for sink to read it before exiting
