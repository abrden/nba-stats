import pickle

import zmq


class ReducerMiddleware:
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

    def __init__(self, endpoint, reducer_mw_ready_endpoint, keys_endpoint, reducer_handler_ready_endpoint,
                 sink_endpoint):
        self.mw = self.MiddlewareConnection(endpoint, reducer_mw_ready_endpoint)
        self.handler_conn = self.ReducerHandlerConnection(keys_endpoint, reducer_handler_ready_endpoint)
        self.sink_conn = self.SinkConnection(sink_endpoint)

    def receive_key(self):
        return self.handler_conn.receive_key()

    def register_key(self, key):
        self.mw.register_key(key)

    def mw_signal_ready(self):
        self.mw.signal_ready()

    def receive(self):
        return self.mw.receive()

    def send_result(self, acc):
        self.sink_conn.send_result(acc)
