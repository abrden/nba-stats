import logging

import zmq

from .dataset_handler import DatasetHandler


class DataVentilator:

    class VentilatorsConnection:
        def __init__(self, mapper_endpoint_1, mapper_endpoint_2, mapper_endpoint_3, dispatcher_ready_endpoint):
            self.logger = logging.getLogger("VentilatorsConnection")

            context = zmq.Context()

            self.ack_server = context.socket(zmq.PULL)
            self.ack_server.bind(dispatcher_ready_endpoint)

            self.server_1 = context.socket(zmq.PUSH)
            self.server_1.bind(mapper_endpoint_1)

            self.server_2 = context.socket(zmq.PUSH)
            self.server_2.bind(mapper_endpoint_2)

            self.server_3 = context.socket(zmq.PUSH)
            self.server_3.bind(mapper_endpoint_3)

        def wait_for_ventilators(self):
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

    def __init__(self, ventilator_endpoint_1, ventilator_endpoint_2, ventilator_endpoint_3, dispatcher_ready_endpoint, dataset_dir):
        self.logger = logging.getLogger("Trigger")
        self.ventilator_endpoint_1 = ventilator_endpoint_1
        self.ventilator_endpoint_2 = ventilator_endpoint_2
        self.ventilator_endpoint_3 = ventilator_endpoint_3
        self.dispatcher_ready_endpoint = dispatcher_ready_endpoint
        self.dataset_dir = dataset_dir

    def start(self):
        ventilators_conn = self.VentilatorsConnection(self.ventilator_endpoint_1,
                                                      self.ventilator_endpoint_2,
                                                      self.ventilator_endpoint_3,
                                                      self.dispatcher_ready_endpoint)
        self.logger.debug("Waiting for ventilators")
        ventilators_conn.wait_for_ventilators()

        self.logger.debug("Sending data to mappers")
        set_handler = DatasetHandler(self.dataset_dir)

        shotlogs = set_handler.get_shotlogs()
        for log in shotlogs:
            self.logger.debug("Reading shotlog: %s", log)
            with open(log, "r") as file:
                header = file.readline()
                line = file.readline()
                while line:
                    self.logger.debug("Read line: %s", line)
                    ventilators_conn.send_shotlog(line)
                    line = file.readline()

        ventilators_conn.close()
