import logging

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


class DataVentilatorMiddleware:

    class ShotlogDisparchersConnection:
        def __init__(self, ventilator_endpoint_1, ventilator_endpoint_2, ventilator_endpoint_3, dispatcher_ready_endpoint):
            self.logger = logging.getLogger("VentilatorsConnection")

            context = zmq.Context()

            self.ack_server = context.socket(zmq.PULL)
            self.ack_server.bind(dispatcher_ready_endpoint)

            self.server_1 = context.socket(zmq.PUSH)
            self.server_1.bind(ventilator_endpoint_1)

            self.server_2 = context.socket(zmq.PUSH)
            self.server_2.bind(ventilator_endpoint_2)

            self.server_3 = context.socket(zmq.PUSH)
            self.server_3.bind(ventilator_endpoint_3)

        def wait_for_dispatchers(self):
            for _ in range(3):
                self.logger.debug("Waiting for shotlog_dispatcher ACK")
                self.ack_server.recv()
            self.logger.debug("Overall shotlog_dispatcher ACK received")

        def send_shotlog(self, shotlog):
            self.server_1.send_string(shotlog)
            self.server_2.send_string(shotlog)
            self.server_3.send_string(shotlog)

        def close(self):
            self.server_1.send_string("END")
            self.server_2.send_string("END")
            self.server_3.send_string("END")

    def __init__(self, ventilator_endpoint_1, ventilator_endpoint_2, ventilator_endpoint_3, dispatcher_ready_endpoint):
        self.dispatchers_conn = self.ShotlogDisparchersConnection(ventilator_endpoint_1, ventilator_endpoint_2, ventilator_endpoint_3, dispatcher_ready_endpoint)

    def wait_for_dispatchers(self):
        self.dispatchers_conn.wait_for_dispatchers()

    def send_shotlog(self, line):
        self.dispatchers_conn.send_shotlog(line)

    def close(self):
        self.dispatchers_conn.close()
