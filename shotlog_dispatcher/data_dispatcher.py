import logging

import zmq


class DataDispatcher:

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
            self.sender.send(data)

        def close(self):
            for _ in range(self.mappers):
                self.sender.send_string("END")

    class EntryConnection:
        def __init__(self, endpoint, dispatcher_ready_endpoint):
            context = zmq.Context()

            self.client = context.socket(zmq.PULL)
            self.client.connect(endpoint)

            ready_ack = context.socket(zmq.PUSH)
            ready_ack.connect(dispatcher_ready_endpoint)

            # Send something to indicate I'm already connected
            ready_ack.send_string("READY")

        def receive_shotlog(self):
            return self.client.recv()

    def __init__(self, mappers, ventilator_endpoint, dispatcher_ready_endpoint, mappers_ready_endpoint, entry_signal_endpoint):
        self.logger = logging.getLogger("DataVentilator")
        self.mappers = mappers
        self.ventilator_endpoint = ventilator_endpoint
        self.dispatcher_ready_endpoint = dispatcher_ready_endpoint
        self.mappers_ready_endpoint = mappers_ready_endpoint
        self.entry_signal_endpoint = entry_signal_endpoint
        self.mappers_conn = None
        self.entry_conn = None

    def start(self):
        self.entry_conn = self.EntryConnection(self.entry_signal_endpoint, self.dispatcher_ready_endpoint)
        self.mappers_conn = self.MappersConnection(self.mappers, self.ventilator_endpoint, self.mappers_ready_endpoint)

        self.logger.debug("Sending data to mappers")
        while True:
            self.logger.debug("Receiving shotlog")
            log = self.entry_conn.receive_shotlog()
            if log == b"END":
                self.logger.debug("Entry END received")
                break
            self.logger.debug("Received shotlog: %r. Sending it to mapper", log)
            self.mappers_conn.send(log)
            self.logger.debug("Received shotlog sent to mapper")

        self.logger.debug("Sending END to mappers")
        self.mappers_conn.close()
