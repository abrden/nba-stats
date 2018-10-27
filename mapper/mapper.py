from multiprocessing import Process
import logging
import random

import zmq


class Mapper(Process):

    class VentilatorConnection:
        def __init__(self, ventilator_endpoint, mappers_ready_endpoint):
            context = zmq.Context()

            self.receiver = context.socket(zmq.PULL)
            self.receiver.connect(ventilator_endpoint)

            mappers_ready_ack = context.socket(zmq.PUSH)
            mappers_ready_ack.connect(mappers_ready_endpoint)
            mappers_ready_ack.send(b"READY")

        def receive_task(self):
            return self.receiver.recv()

    class MiddlewareConnection:
        def __init__(self, mw_endpoint, key_queue_endpoint):
            context = zmq.Context()

            self.mw_socket = context.socket(zmq.REQ)
            self.mw_socket.setsockopt(zmq.REQ_RELAXED, 1)
            self.mw_socket.setsockopt(zmq.REQ_CORRELATE, 1)
            self.mw_socket.connect(mw_endpoint)

            self.key_queue_socket = context.socket(zmq.PUSH)
            self.key_queue_socket.connect(key_queue_endpoint)

        def send(self, data):
            return self.mw_socket.send(data)

        def notify_key(self, key):
            return self.key_queue_socket.send(key)

    def __init__(self, mw_endpoint, key_queue_endpoint, ventilator_endpoint, mappers_ready_endpoint):
        super().__init__()
        self.logger = logging.getLogger("Mapper")
        self.mw_endpoint = mw_endpoint
        self.key_queue_endpoint = key_queue_endpoint
        self.ventilator_endpoint = ventilator_endpoint
        self.mappers_ready_endpoint = mappers_ready_endpoint
        self.ventilator_conn = None
        self.mw = None

    def run(self):
        self.ventilator_conn = self.VentilatorConnection(self.ventilator_endpoint, self.mappers_ready_endpoint)
        self.mw = self.MiddlewareConnection(self.mw_endpoint, self.key_queue_endpoint)  # FIXME doesnt work if I initialize it on the constructor

        while True:
            self.logger.debug("Waiting for task from ventilator")
            task = self.ventilator_conn.receive_task()
            if task == b"END":
                self.logger.debug("END received")
                self.mw.notify_key(b"END")
                self.mw.send(b"END")
                return
            self.logger.debug("Task received: %s", task)
            key = random.choice([b'A', b'B'])
            value = task
            self.logger.debug("Emitting result: (%s, %s)", key, value)
            self.mw.notify_key(key)
            self.mw.send(key + "#".encode() + value)
