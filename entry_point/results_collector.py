import logging

from middleware.entry import ResultsCollectorMiddleware


class ResultsCollector:

    def __init__(self, endpoint):
        self.logger = logging.getLogger("ResultsCollector")
        self.conn = ResultsCollectorMiddleware(endpoint)

    def start(self):
        results = []
        for _ in range(4):
            self.logger.debug("Receiving result")
            result = self.conn.receive_result()
            self.logger.debug("Result received: %r", result)
            results.append(result)

        self.conn.close()
        return results
