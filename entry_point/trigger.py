import logging

import zmq


class Trigger:

    class VentilatorsConnection:
        def __init__(self, ventilator_endpoint_1, ventilator_endpoint_2, ventilator_endpoint_3):
            self.logger = logging.getLogger("VentilatorsConnection")

            context = zmq.Context()

            self.server_1 = context.socket(zmq.REP)
            self.server_1.bind(ventilator_endpoint_1)

            self.server_2 = context.socket(zmq.REP)
            self.server_2.bind(ventilator_endpoint_2)

            self.server_3 = context.socket(zmq.REP)
            self.server_3.bind(ventilator_endpoint_3)

        def wait_for_ventilators(self):
            self.logger.debug("Waiting for ventilator 1")
            #self.server_1.recv()
            #self.logger.debug("Ventilator 1 ready. Waiting for ventilator 2") TODO uncomment when implemented
            msg = self.server_2.recv()
            self.logger.debug("Ventilator 2 ready %r", msg)
            #self.logger.debug("Ventilator 1 and 2 ready. Waiting for ventilator 3")
            #self.server_3.recv()

        def signal_ventilators(self):
            #self.server_1.send_string("START")
            self.server_2.send_string("START")
            #self.server_3.send_string("START")

    def __init__(self, ventilator_endpoint_1, ventilator_endpoint_2, ventilator_endpoint_3):
        self.logger = logging.getLogger("Trigger")
        self.ventilator_endpoint_1 = ventilator_endpoint_1
        self.ventilator_endpoint_2 = ventilator_endpoint_2
        self.ventilator_endpoint_3 = ventilator_endpoint_3

    def start(self):
        ventilators_conn = self.VentilatorsConnection(self.ventilator_endpoint_1,
                                                      self.ventilator_endpoint_2,
                                                      self.ventilator_endpoint_3)
        self.logger.debug("Waiting for ventilators")
        ventilators_conn.wait_for_ventilators()
        self.logger.debug("Signaling ventilators to start")
        ventilators_conn.signal_ventilators()
