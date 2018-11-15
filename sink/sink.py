import logging

from middleware.sink import SinkMiddleware


class DataSink:

    def __init__(self, endpoint, collector_endpoint, reducer_spawner_endpoint, ventilator_endpoint=None, dispatcher_ready_endpoint=None):
        self.logger = logging.getLogger("DataSink")
        self.retroalimentation = False
        if ventilator_endpoint and dispatcher_ready_endpoint:
            self.retroalimentation = True
        self.conn = SinkMiddleware(endpoint, collector_endpoint, reducer_spawner_endpoint, ventilator_endpoint, dispatcher_ready_endpoint)

    def start(self, fun):

        self.logger.debug("Receiving reducers quantity")
        reducers = self.conn.receive_reducers_number()
        self.logger.debug("Reducers quantity received: %d", reducers)

        results_received = 0
        results = []
        while True:
            self.logger.debug("Receiving result from reducers")
            result = self.conn.receive_reducer_result()
            self.logger.debug("Result received %r", result)

            results.append(result)
            results_received += 1

            if results_received == reducers:
                self.logger.debug("All results have been received")
                break

        self.logger.debug("Formatting results")
        ans = fun(results)

        self.logger.debug("Sending results to collector")
        self.conn.send_result(ans)

        if self.retroalimentation:
            self.logger.debug("Sending results to dispatcher")
            for result in ans:
                self.conn.dispatcher_send_result(result)
            self.conn.dispatcher_close()
