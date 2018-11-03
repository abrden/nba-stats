import logging
import pickle

import zmq


class DataSink:

    class ReducersConnection:
        def __init__(self, endpoint):
            context = zmq.Context()
            self.server = context.socket(zmq.PULL)
            self.server.bind(endpoint)

        def receive_reducer_result(self):
            b_data = self.server.recv()
            return pickle.loads(b_data)

    class ReducerSpawnerConnection:
        def __init__(self, endpoint):
            context = zmq.Context()
            self.server = context.socket(zmq.REP)
            self.server.bind(endpoint)

        def receive_reducers_number(self):
            return int(self.server.recv().decode())

    class CollectorConnection:
        def __init__(self, endpoint):
            self.logger = logging.getLogger("CollectorConnection")

            context = zmq.Context()
            self.client = context.socket(zmq.PUSH)
            self.client.connect(endpoint)

        def send_result(self, result):
            r = str(result)
            self.logger.debug("Sending final result to collector: %r", r)
            self.client.send_string(r)

    def __init__(self, endpoint, collector_endpoint):
        self.logger = logging.getLogger("DataSink")
        self.endpoint = endpoint
        self.collector_endpoint = collector_endpoint
        self.reducers_conn = None
        self.collector_conn = None

    def start(self, reducer_spawner_endpoint, fun):
        self.reducers_conn = self.ReducersConnection(self.endpoint)
        self.collector_conn = self.CollectorConnection(self.collector_endpoint)

        reducer_spawner_conn = self.ReducerSpawnerConnection(reducer_spawner_endpoint)
        self.logger.debug("Receiving reducers quantity")
        reducers = reducer_spawner_conn.receive_reducers_number()
        self.logger.debug("Reducers quantity received: %d", reducers)

        results_received = 0
        results = []
        while True:
            self.logger.debug("Receiving result from reducers")
            result = self.reducers_conn.receive_reducer_result()
            self.logger.debug("Result received %r", result)

            results.append(result)

            results_received += 1

            if results_received == reducers:
                self.logger.debug("All results have been received")
                break

        ans = fun(results)

        self.collector_conn.send_result(ans)
