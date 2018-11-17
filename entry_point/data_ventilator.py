import logging

from .dataset_handler import DatasetHandler
from middleware.entry import DataVentilatorMiddleware


class DataVentilator:

    def __init__(self, ventilator_endpoint_1, ventilator_endpoint_2, ventilator_endpoint_3, dispatcher_ready_endpoint, dataset_dir):
        self.logger = logging.getLogger("DataVentilator")
        self.dataset_dir = dataset_dir
        self.conn = DataVentilatorMiddleware(ventilator_endpoint_1, ventilator_endpoint_2, ventilator_endpoint_3, dispatcher_ready_endpoint)

    def start(self):
        self.logger.debug("Waiting for dispatchers")
        self.conn.wait_for_dispatchers()

        self.logger.debug("Sending data to dispatchers")
        set_handler = DatasetHandler(self.dataset_dir)

        shotlogs = set_handler.get_shotlogs()
        for log in shotlogs:
            self.logger.debug("Reading shotlog: %s", log)
            with open(log, "r") as file:
                header = file.readline()
                line = file.readline()
                while line:
                    self.logger.debug("Read line: %s", line)
                    self.conn.send_shotlog(line)
                    line = file.readline()

        self.conn.close()
