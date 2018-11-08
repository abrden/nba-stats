import logging
import pickle

import zmq


class Middleware:

    class ReducersConnection:
        def __init__(self, reducers_ready_endpoint, reducers):
            self.logger = logging.getLogger("ReducersConnection")
            self.reducers = reducers

            context = zmq.Context()

            self.client = context.socket(zmq.PULL)
            self.client.bind(reducers_ready_endpoint)

        def wait_for_reducers_to_connect(self):
            for _ in range(self.reducers):
                self.client.recv()
                self.logger.debug("Reducer ACK received")

    class Connection:
        def __init__(self, endpoint):
            self.logger = logging.getLogger("MappersConnection")

            context = zmq.Context()
            self.server = context.socket(zmq.ROUTER)
            self.server.bind(endpoint)

        def receive_mapper_pair(self):
            b_message = self.server.recv_multipart()  # FIXME why do I have to recv a multipart if mapper sent me a string
            message = pickle.loads(b_message[3])
            self.logger.debug("Pyobj received %r", message)
            return message

        def send_value_to_reducer(self, key, value):
            b_key = str(key).encode()
            b_value = pickle.dumps(value, -1)
            self.server.send_multipart([b_key, b_value])

        def close_conn_with_reducers(self, reducers):
            for key in reducers:
                self.send_value_to_reducer(key, "END")

    def __init__(self, mappers, reducers, endpoint, reducer_ready_endpoint):
        self.logger = logging.getLogger("Middleware")

        self.mappers = mappers
        self.reducers = reducers
        self.endpoint = endpoint
        self.reducer_ready_endpoint = reducer_ready_endpoint
        self.reducers_conn = None
        self.conn = None

    def start(self):
        self.reducers_conn = self.ReducersConnection(self.reducer_ready_endpoint, self.reducers)
        self.conn = self.Connection(self.endpoint)

        self.logger.debug("Waiting for reducer spawner signal")
        self.reducers_conn.wait_for_reducers_to_connect()
        self.logger.debug("Signal received, sending data to reducers")

        keys = {}
        ends_received = 0
        while True:
            self.logger.debug("Receiving message from mappers")
            message = self.conn.receive_mapper_pair()

            if message == b"END":
                self.logger.debug("END received")
                ends_received += 1
                if ends_received == self.mappers:
                    break
                else:
                    continue

            key, value = message

            if key not in keys:
                keys[key] = True

            self.logger.debug("Received key %r and value %r", key, value)
            self.logger.debug("Sending message to reducer")
            self.conn.send_value_to_reducer(key, value)
            self.logger.debug("Task sent")

        self.logger.debug("Sending END to reducers")
        self.conn.close_conn_with_reducers(keys)
