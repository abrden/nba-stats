import logging

from middleware.pair_dispatcher import PairDispatcherMiddleware


class PairDispatcher:

    def __init__(self, mappers, reducers, endpoint, reducer_ready_endpoint):
        self.logger = logging.getLogger("PairDispatcher")
        self.mappers = mappers
        self.conn = PairDispatcherMiddleware(reducers, endpoint, reducer_ready_endpoint)

    def start(self):
        self.logger.debug("Waiting for reducer spawner signal")
        self.conn.wait_for_reducers_to_connect()
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

        self.logger.debug("Sending END to reducers: %r", keys)
        self.conn.close_reducers_conn(keys)
