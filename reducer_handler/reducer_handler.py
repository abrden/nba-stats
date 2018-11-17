import logging

from middleware.reducer_handler import ReducerHandlerMiddleware


class ReducerHandler:

    def __init__(self, mappers, reducers, key_queue_endpoint, keys_to_reducers_endpoint, reducers_ready_endpoint, sink_endpoint):
        self.logger = logging.getLogger("ReducerSpawner")
        self.reducers_keys = {}
        self.reducers = reducers
        self.mappers = mappers
        self.conn = ReducerHandlerMiddleware(reducers, key_queue_endpoint, keys_to_reducers_endpoint, reducers_ready_endpoint, sink_endpoint)

    def start(self):
        self.logger.debug("Distributing keys to reducers")
        ends_received = 0
        while True:
            self.logger.debug("Receiving key from mapper")
            key = self.conn.receive_key()
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
                self.conn.send_key(key)
                self.reducers_keys[key] = 'dummy'

        self.logger.debug("The keys received were: %r", self.reducers_keys.keys())
        self.conn.close_reducers_connection()

        self.logger.debug("Sending keys quantity to Sink")
        self.conn.notify_reducers_quantity(len(self.reducers_keys))
