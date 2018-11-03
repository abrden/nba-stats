import logging

import zmq


class ResultsCollector:

    class SinksConnection:
        def __init__(self, endpoint):
            context = zmq.Context()
            self.server = context.socket(zmq.PULL)
            self.server.bind(endpoint)

        def receive_result(self):
            return self.server.recv()

    def __init__(self, endpoint):
        self.logger = logging.getLogger("ResultsCollector")

        self.endpoint = endpoint
        self.sinks_conn = None

    def start(self):
        self.sinks_conn = self.SinksConnection(self.endpoint)

        results = []
        for _ in range(2):  # TODO receive the results of all operations
            self.logger.debug("Receiving result")
            result = self.sinks_conn.receive_result()
            self.logger.debug("Result received: %r", result)
            results.append(result)

        return results
