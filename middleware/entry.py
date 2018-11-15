import zmq


class ResultsCollectorMiddleware:

    class SinksConnection:
        def __init__(self, endpoint):
            context = zmq.Context()
            self.server = context.socket(zmq.PULL)
            self.server.bind(endpoint)

        def receive_result(self):
            return self.server.recv()

    def __init__(self, endpoint):
        self.sinks_conn = self.SinksConnection(endpoint)

    def receive_result(self):
        return self.sinks_conn.receive_result()
