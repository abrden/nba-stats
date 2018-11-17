import logging
import pickle

import zmq


class SinkMiddleware:

    class ReducersConnection:
        def __init__(self, endpoint):
            context = zmq.Context()
            self.server = context.socket(zmq.PULL)
            self.server.bind(endpoint)

        def receive_reducer_result(self):
            b_data = self.server.recv()
            return pickle.loads(b_data)

        def close(self):
            self.server.close()

    class ReducerHandlerConnection:
        def __init__(self, endpoint):
            context = zmq.Context()
            self.server = context.socket(zmq.REP)
            self.server.bind(endpoint)

        def receive_reducers_number(self):
            return int(self.server.recv().decode())

        def close(self):
            self.server.close()

    class CollectorConnection:
        def __init__(self, endpoint):
            self.logger = logging.getLogger("CollectorConnection")

            context = zmq.Context()
            self.client = context.socket(zmq.PUSH)
            self.client.setsockopt(zmq.LINGER, -1)
            self.client.connect(endpoint)

        def send_result(self, result):
            r = str(result)
            self.logger.debug("Sending final result to collector: %r", r)
            self.client.send_string(r)

        def close(self):
            self.client.close()

    class DispatcherConnection:
        def __init__(self, endpoint, dispatcher_ready_endpoint):
            self.logger = logging.getLogger("DispatcherConnection")

            context = zmq.Context()

            self.server = context.socket(zmq.PUSH)
            self.server.setsockopt(zmq.LINGER, -1)
            self.server.bind(endpoint)

            ack_server = context.socket(zmq.PULL)
            ack_server.bind(dispatcher_ready_endpoint)
            ack_server.recv()
            self.logger.debug("Dispatcher ACK received")
            ack_server.close()

        def send_result(self, result):
            self.logger.debug("Sending result to dispatcher: %r", result)
            b_result = str(result)
            self.server.send_string(b_result)

        def close(self):
            self.server.send_string("END")
            self.server.close()

    def __init__(self, endpoint, collector_endpoint, reducer_spawner_endpoint, ventilator_endpoint=None, dispatcher_ready_endpoint=None):
        self.logger = logging.getLogger("SinkMiddleware")
        self.reducers_conn = self.ReducersConnection(endpoint)
        self.collector_conn = self.CollectorConnection(collector_endpoint)
        if ventilator_endpoint and dispatcher_ready_endpoint:
            self.dispatcher_conn = self.DispatcherConnection(ventilator_endpoint, dispatcher_ready_endpoint)
        self.reducer_handler_conn = self.ReducerHandlerConnection(reducer_spawner_endpoint)

    def receive_reducers_number(self):
        return self.reducer_handler_conn.receive_reducers_number()

    def receive_reducer_result(self):
        return self.reducers_conn.receive_reducer_result()

    def send_result(self, ans):
        self.collector_conn.send_result(ans)

    def dispatcher_send_result(self, result):
        self.dispatcher_conn.send_result(result)

    def dispatcher_close(self):
        self.dispatcher_conn.close()

    def close(self):
        self.reducer_handler_conn.close()
        self.reducers_conn.close()
        self.collector_conn.close()