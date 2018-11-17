import logging
import pickle

import zmq


class PairDispatcherMiddleware:

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
            self.client.close()

    class Connection:
        def __init__(self, endpoint):
            self.logger = logging.getLogger("MappersConnection")

            context = zmq.Context()
            self.server = context.socket(zmq.ROUTER)
            self.server.setsockopt(zmq.LINGER, -1)
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
            self.server.close()

    def __init__(self, reducers, endpoint, reducer_ready_endpoint):
        self.reducers_conn = self.ReducersConnection(reducer_ready_endpoint, reducers)
        self.conn = self.Connection(endpoint)

    def wait_for_reducers_to_connect(self):
        self.reducers_conn.wait_for_reducers_to_connect()

    def receive_mapper_pair(self):
        return self.conn.receive_mapper_pair()

    def send_value_to_reducer(self, key, value):
        self.conn.send_value_to_reducer(key, value)

    def close_reducers_conn(self, keys):
        self.conn.close_conn_with_reducers(keys)
