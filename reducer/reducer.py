import logging

from middleware.reducer import ReducerMiddleware


class Reducer:

    def __init__(self, endpoint, reducer_mw_ready_endpoint, keys_endpoint,
                 reducer_handler_ready_endpoint, sink_endpoint):
        self.logger = logging.getLogger("Reducer")
        self.acc = {}
        self.conn = ReducerMiddleware(endpoint, reducer_mw_ready_endpoint, keys_endpoint,
                                      reducer_handler_ready_endpoint, sink_endpoint)

    def start(self, fun):
        acc = {}

        self.logger.debug("Receiving keys")
        while True:
            self.logger.debug("Receiving key from ReducerHandler")
            key = self.conn.receive_key()
            if key == b'END':
                self.logger.debug("ReducerHandler END received")
                break
            self.logger.debug("Receiving key: %r", key)
            acc[key] = None
            self.conn.register_key(key)

        self.logger.debug("Signaling MW")
        self.conn.mw_signal_ready()

        self.logger.debug("Working with values")
        ends_received = 0
        while True:
            self.logger.debug("Receiving")
            pairs = self.conn.receive()
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
        self.conn.send_result(acc)

        self.conn.close()
