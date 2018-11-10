import logging

import zmq


class ReducerHandler:

    class MappersConnection:
        def __init__(self, key_queue_endpoint):
            context = zmq.Context()

            self.server = context.socket(zmq.PULL)
            self.server.bind(key_queue_endpoint)

        def receive_key(self):
            return self.server.recv()

    class ReducersConnection:
        def __init__(self, reducers, endpoint, reducers_ready_endpoint):
            context = zmq.Context()
            self.reducers = reducers
            self.logger = logging.getLogger("ReducersConnection")

            self.socket = context.socket(zmq.PUSH)
            self.socket.bind(endpoint)

            reducers_ready_ack = context.socket(zmq.PULL)
            reducers_ready_ack.bind(reducers_ready_endpoint)

            self.logger.debug("Waiting for reducers ready ACK")
            for _ in range(self.reducers):
                ack = reducers_ready_ack.recv()
                self.logger.debug("Reducer ACK received: %r", ack)

        def send_key(self, key):
            self.logger.debug("Sending key to reducer")
            self.socket.send(key)
            self.logger.debug("Sent key to reducer")

        def close(self):
            for _ in range(self.reducers):
                self.socket.send_string("END")

    class SinkConnection:
        def __init__(self, endpoint):
            context = zmq.Context()

            self.client = context.socket(zmq.REQ)
            self.client.connect(endpoint)

        def notify_reducers_quantity(self, reducers):
            self.client.send_string(str(reducers))

    def __init__(self, mappers, reducers, key_queue_endpoint, keys_to_reducers_endpoint, reducers_ready_endpoint, sink_endpoint):
        self.logger = logging.getLogger("ReducerSpawner")
        self.reducers_keys = {}
        self.reducers = reducers
        self.mappers = mappers
        self.key_queue_endpoint = key_queue_endpoint
        self.keys_to_reducers_endpoint = keys_to_reducers_endpoint
        self.reducers_ready_endpoint = reducers_ready_endpoint
        self.sink_endpoint = sink_endpoint
        self.mw_conn = None
        self.mappers_conn = None
        self.sink_conn = None
        self.reducers_conn = None

    def start(self):
        self.mappers_conn = self.MappersConnection(self.key_queue_endpoint)
        self.sink_conn = self.SinkConnection(self.sink_endpoint)
        self.reducers_conn = self.ReducersConnection(self.reducers, self.keys_to_reducers_endpoint, self.reducers_ready_endpoint)

        self.logger.debug("Distributing keys to reducers")
        ends_received = 0
        while True:
            self.logger.debug("Receiving key from mapper")
            key = self.mappers_conn.receive_key()
            self.logger.debug("Received key: %r", key)
            if key == b"END":
                self.logger.debug("END received")
                ends_received += 1
                if ends_received == self.mappers:
                    break
            elif key in self.reducers_keys:
                self.logger.debug("A reducer is already designated for key: %r", key)
            else:
                self.logger.debug("Designating to reducer")
                self.reducers_conn.send_key(key)
                self.reducers_keys[key] = 'dummy'

        self.logger.debug("The keys received were: %r", self.reducers_keys.keys())
        self.reducers_conn.close()

        self.logger.debug("Sending keys quantity to Sink")
        self.sink_conn.notify_reducers_quantity(len(self.reducers_keys))
