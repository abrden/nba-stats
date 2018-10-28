import logging

import zmq

from .dataset_handler import DatasetHandler


class DataVentilator:

    class MappersConnection:
        def __init__(self, mappers, ventilator_endpoint, mappers_ready_endpoint):
            self.mappers = mappers
            self.logger = logging.getLogger("MapperConnection")

            context = zmq.Context()

            self.sender = context.socket(zmq.PUSH)
            self.sender.bind(ventilator_endpoint)

            mappers_ready_ack = context.socket(zmq.PULL)
            mappers_ready_ack.bind(mappers_ready_endpoint)

            self.logger.debug("Waiting for mappers ready ACK")
            for _ in range(self.mappers):
                ack = mappers_ready_ack.recv()
                self.logger.debug("Mapper ACK received: %r", ack)

        def send(self, data):
            self.sender.send_string(data)

        def close(self):
            for _ in range(self.mappers):
                self.sender.send_string("END")

    def __init__(self, mappers, ventilator_endpoint, mappers_ready_endpoint):
        self.logger = logging.getLogger("DataVentilator")
        self.mappers = mappers
        self.ventilator_endpoint = ventilator_endpoint
        self.mappers_ready_endpoint = mappers_ready_endpoint
        self.mappers_conn = None

    def start(self, dataset_dir):
        self.mappers_conn = self.MappersConnection(self.mappers, self.ventilator_endpoint, self.mappers_ready_endpoint)

        self.logger.debug("Sending data to mappers")
        set_handler = DatasetHandler(dataset_dir)

        shotlogs = set_handler.get_shotlogs()
        for log in shotlogs:
            self.logger.debug("Reading shotlog: %s", log)
            with open(log, "r") as file:
                header = file.readline()
                line = file.readline()
                while line:
                    self.logger.debug("Read line: %s", line)
                    self.mappers_conn.send(line)
                    line = file.readline()

        self.mappers_conn.close()
