import logging

import zmq


class Middleware:

    class ReducerSpawnerConnection:
        def __init__(self, reducer_spawner_endpoint):
            context = zmq.Context()

            self.client = context.socket(zmq.REP)
            self.client.bind(reducer_spawner_endpoint)

        def wait_for_reducers_to_connect(self):
            self.client.recv()

    class Connection:
        def __init__(self, endpoint):
            self.logger = logging.getLogger("MappersConnection")

            context = zmq.Context()
            self.server = context.socket(zmq.ROUTER)
            self.server.bind(endpoint)

        def receive_mapper_pair(self):
            message = self.server.recv_multipart()  # FIXME why do I have to recv a multipart if mapper sent me a string
            self.logger.debug("Multipart received %r", message)
            return message[3]

        def send_value_to_reducer(self, key, value):
            self.server.send_multipart([key, value])

        def close_conn_with_reducers(self, reducers):
            for key in reducers:
                self.server.send_multipart([key, b'END'])

    def __init__(self, mappers, endpoint, reducer_spawner_endpoint):
        self.logger = logging.getLogger("Middleware")

        self.mappers = mappers
        self.endpoint = endpoint
        self.reducer_spawner_endpoint = reducer_spawner_endpoint
        self.reducer_spawner_conn = None
        self.conn = None

    def start(self):
        self.reducer_spawner_conn = self.ReducerSpawnerConnection(self.reducer_spawner_endpoint)
        self.conn = self.Connection(self.endpoint)

        self.logger.debug("Waiting for reducer spawner signal")
        self.reducer_spawner_conn.wait_for_reducers_to_connect()
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

            key, value = message.split('#'.encode())

            if key not in keys:
                keys[key] = True

            self.logger.debug("Received key %r and value %r", key, value)
            self.logger.debug("Sending message to reducer")
            self.conn.send_value_to_reducer(key, value)
            self.logger.debug("Task sent")

        self.logger.debug("Sending END to reducers")
        self.conn.close_conn_with_reducers(keys)
