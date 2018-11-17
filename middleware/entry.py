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

        def close(self):
            self.server.close()

    def __init__(self, endpoint):
        self.sinks_conn = self.SinksConnection(endpoint)

    def receive_result(self):
        return self.sinks_conn.receive_result()

    def close(self):
        self.sinks_conn.close()


class DataVentilatorMiddleware:

    class ShotlogDisparchersConnection:
        def __init__(self, ventilator_endpoint_1, ventilator_endpoint_2, ventilator_endpoint_3, dispatcher_ready_endpoint):
            self.logger = logging.getLogger("VentilatorsConnection")

            self.context = zmq.Context()

            self.ack_server = self.context.socket(zmq.PULL)
            self.ack_server.bind(dispatcher_ready_endpoint)

            self.server_1 = self.context.socket(zmq.PUSH)
            self.server_1.setsockopt(zmq.LINGER, -1)
            self.server_1.bind(ventilator_endpoint_1)

            self.server_2 = self.context.socket(zmq.PUSH)
            self.server_2.setsockopt(zmq.LINGER, -1)
            self.server_2.bind(ventilator_endpoint_2)

            self.server_3 = self.context.socket(zmq.PUSH)
            self.server_3.setsockopt(zmq.LINGER, -1)
            self.server_3.bind(ventilator_endpoint_3)

        def wait_for_dispatchers(self):
            for _ in range(3):
                self.logger.debug("Waiting for shotlog_dispatcher ACK")
                self.ack_server.recv()
            self.logger.debug("Overall shotlog_dispatcher ACK received")
            self.ack_server.close()

        def send_shotlog(self, shotlog):
            self.server_1.send_string(shotlog)
            self.server_2.send_string(shotlog)
            self.server_3.send_string(shotlog)

        def close(self):
            self.logger.debug("Done with the dataset. Sending END to shotlog_dispatchers")
            self.server_1.send_string("END")
            self.server_2.send_string("END")
            self.server_3.send_string("END")

            self.logger.debug("Closing sockets")
            self.server_1.close()
            self.server_2.close()
            self.server_3.close()

            # Context terminated by ResultsCollectorMiddleware

    def __init__(self, ventilator_endpoint_1, ventilator_endpoint_2, ventilator_endpoint_3, dispatcher_ready_endpoint):
        self.dispatchers_conn = self.ShotlogDisparchersConnection(ventilator_endpoint_1, ventilator_endpoint_2, ventilator_endpoint_3, dispatcher_ready_endpoint)

    def wait_for_dispatchers(self):
        self.dispatchers_conn.wait_for_dispatchers()

    def send_shotlog(self, line):
        self.dispatchers_conn.send_shotlog(line)

    def close(self):
        self.dispatchers_conn.close()
