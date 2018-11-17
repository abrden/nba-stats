import pickle

import zmq


class MapperMiddleware:

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

    class ReducerSpawnerConnection:
        def __init__(self, key_queue_endpoint):
            context = zmq.Context()

            self.key_queue_socket = context.socket(zmq.PUSH)
            self.key_queue_socket.connect(key_queue_endpoint)

        def notify_key(self, key):
            self.key_queue_socket.send_string(str(key))

        def close(self):
            self.key_queue_socket.send_string("END")

    class MiddlewareConnection:
        def __init__(self, mw_endpoint):
            context = zmq.Context()

            self.mw_socket = context.socket(zmq.REQ)
            self.mw_socket.setsockopt(zmq.REQ_RELAXED, 1)
            self.mw_socket.setsockopt(zmq.REQ_CORRELATE, 1)
            self.mw_socket.connect(mw_endpoint)

        def send(self, data):
            b_data = pickle.dumps(data, -1)
            self.mw_socket.send(b_data)

        def close(self):
            self.send(b"END")

    def __init__(self, mw_endpoint, key_queue_endpoint, ventilator_endpoint, mappers_ready_endpoint):
        self.mw_endpoint = mw_endpoint
        self.key_queue_endpoint = key_queue_endpoint
        self.ventilator_endpoint = ventilator_endpoint
        self.mappers_ready_endpoint = mappers_ready_endpoint
        self.ventilator_conn = self.VentilatorConnection(self.ventilator_endpoint, self.mappers_ready_endpoint)
        self.reducer_spawner_conn = self.ReducerSpawnerConnection(self.key_queue_endpoint)
        self.mw = self.MiddlewareConnection(self.mw_endpoint)

    def receive_task(self):
        return self.ventilator_conn.receive_task()

    def notify_key(self, key):
        self.reducer_spawner_conn.notify_key(key)

    def send(self, data):
        self.mw.send(data)

    def dispatcher_and_handler_close(self):
        self.reducer_spawner_conn.close()
        self.mw.close()
