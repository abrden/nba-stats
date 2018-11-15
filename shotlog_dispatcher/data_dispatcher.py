import logging

from middleware.shotlog_dispatcher import ShotlogDispatcherMiddleware


class DataDispatcher:

    def __init__(self, mappers, ventilator_endpoint, dispatcher_ready_endpoint, mappers_ready_endpoint, entry_signal_endpoint):
        self.logger = logging.getLogger("DataVentilator")
        self.conn = ShotlogDispatcherMiddleware(mappers, ventilator_endpoint, dispatcher_ready_endpoint, mappers_ready_endpoint, entry_signal_endpoint)

    def start(self):
        self.logger.debug("Sending data to mappers")
        while True:
            self.logger.debug("Receiving shotlog")
            log = self.conn.receive_shotlog()
            if log == b"END":
                self.logger.debug("Entry END received")
                break
            self.logger.debug("Received shotlog: %r. Sending it to mapper", log)
            self.conn.send(log)
            self.logger.debug("Received shotlog sent to mapper")

        self.logger.debug("Sending END to mappers")
        self.conn.close()
