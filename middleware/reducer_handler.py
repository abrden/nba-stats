import logging

import zmq


class ReducerHandlerMiddleware:

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

    def __init__(self, reducers, key_queue_endpoint, keys_to_reducers_endpoint, reducers_ready_endpoint, sink_endpoint):
        self.mappers_conn = self.MappersConnection(key_queue_endpoint)
        self.sink_conn = self.SinkConnection(sink_endpoint)
        self.reducers_conn = self.ReducersConnection(reducers, keys_to_reducers_endpoint, reducers_ready_endpoint)

    def receive_key(self):
        return self.mappers_conn.receive_key()

    def send_key(self, key):
        self.reducers_conn.send_key(key)

    def close_reducers_connection(self):
        self.reducers_conn.close()

    def notify_reducers_quantity(self, keys_quantity):
        self.sink_conn.notify_reducers_quantity(keys_quantity)
