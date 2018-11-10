import logging
import pickle

import zmq


class ResultsCollector:

    class SinksConnection:
        def __init__(self, endpoint):
            context = zmq.Context()
            self.server = context.socket(zmq.PULL)
            self.server.bind(endpoint)

        def receive_result(self):
            b_result = self.server.recv()
            result = pickle.loads(b_result)
            return result

    def __init__(self, endpoint):
        self.logger = logging.getLogger("ResultsCollector")

        self.endpoint = endpoint
        self.sinks_conn = None

    def start(self):
        self.sinks_conn = self.SinksConnection(self.endpoint)

        results = {}
        for _ in range(3):  # TODO receive the results of all operations
            self.logger.debug("Receiving result")
            result = self.sinks_conn.receive_result()
            self.logger.debug("Result received: %r", result)
            id, result = result
            results[id] = result

        return results
