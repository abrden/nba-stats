import logging

import zmq

from .reducer import Reducer


class ReducerSpawner:

    class MappersConnection:
        def __init__(self, key_queue_endpoint):
            context = zmq.Context()

            self.server = context.socket(zmq.PULL)
            self.server.bind(key_queue_endpoint)

        def receive_key(self):
            return self.server.recv()

    class MiddlewareConnection:
        def __init__(self, reducer_spawner_endpoint, reducers_ready_endpoint):
            self.logger = logging.getLogger("MiddlewareConnection")
            context = zmq.Context()

            self.reducer_spawner_server = context.socket(zmq.REQ)
            self.reducer_spawner_server.connect(reducer_spawner_endpoint)

            self.reducers_ready_server = context.socket(zmq.PULL)
            self.reducers_ready_server.bind(reducers_ready_endpoint)

        def sync_reducers(self, reducers):
            self.logger.debug("Waiting for reducers ready ACK")
            for _ in range(reducers):
                ack = self.reducers_ready_server.recv()
                self.logger.debug("Reducer ACK received: %r", ack)
            self.logger.debug("Sending overall ACK to MW")
            self.reducer_spawner_server.send(b"READY")

    def __init__(self, key_queue_endpoint, reducer_spawner_endpoint, reducers_ready_endpoint):
        self.logger = logging.getLogger("ReducerSpawner")
        self.reducers = {}
        self.key_queue_endpoint = key_queue_endpoint
        self.reducer_spawner_endpoint = reducer_spawner_endpoint
        self.reducers_ready_endpoint = reducers_ready_endpoint
        self.mw_conn = None
        self.mappers_conn = None

    def start(self, mappers, mw_endpoint, fun):
        self.mw_conn = self.MiddlewareConnection(self.reducer_spawner_endpoint, self.reducers_ready_endpoint)
        self.mappers_conn = self.MappersConnection(self.key_queue_endpoint)

        self.logger.debug("Spawning reducers")
        ends_received = 0
        while True:
            self.logger.debug("Receiving key from mapper")
            key = self.mappers_conn.receive_key()
            self.logger.debug("Received key: %r", key)
            if key == b"END":
                self.logger.debug("END received")
                ends_received += 1
                if ends_received == mappers:
                    break
            elif key in self.reducers:
                self.logger.debug("A reducer is already created for key: %r", key)
            else:
                self.logger.debug("Starting new reducer")
                r = Reducer(key, mw_endpoint, self.reducers_ready_endpoint, fun)
                r.start()
                self.reducers[key] = r

        self.mw_conn.sync_reducers(len(self.reducers))

    def close(self):
        self.logger.debug("Joining reducers")
        for key in self.reducers:
            self.logger.debug("Joining reducer with key %r", key)
            self.reducers[key].join()
