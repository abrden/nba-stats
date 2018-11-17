import pickle

import zmq


class MapperMiddleware:

    class ShotlogDispatcherConnection:
        def __init__(self, ventilator_endpoint, mappers_ready_endpoint):
            context = zmq.Context()

            self.receiver = context.socket(zmq.PULL)
            self.receiver.connect(ventilator_endpoint)

            mappers_ready_ack = context.socket(zmq.PUSH)
            mappers_ready_ack.connect(mappers_ready_endpoint)
            mappers_ready_ack.send(b"READY")
            mappers_ready_ack.close()

        def receive_task(self):
            return self.receiver.recv()

        def close(self):
            self.receiver.close()

    class ReducerHandlerConnection:
        def __init__(self, key_queue_endpoint):
            context = zmq.Context()

            self.key_queue_socket = context.socket(zmq.PUSH)
            self.key_queue_socket.setsockopt(zmq.LINGER, -1)
            self.key_queue_socket.connect(key_queue_endpoint)

        def notify_key(self, key):
            self.key_queue_socket.send_string(str(key))

        def close(self):
            self.key_queue_socket.send_string("END")
            self.key_queue_socket.close()

    class PairDispatcherConnection:
        def __init__(self, mw_endpoint):
            context = zmq.Context()

            self.mw_socket = context.socket(zmq.REQ)
            self.mw_socket.setsockopt(zmq.LINGER, -1)
            self.mw_socket.setsockopt(zmq.REQ_RELAXED, 1)
            self.mw_socket.setsockopt(zmq.REQ_CORRELATE, 1)
            self.mw_socket.connect(mw_endpoint)

        def send(self, data):
            b_data = pickle.dumps(data, -1)
            self.mw_socket.send(b_data)

        def close(self):
            self.send(b"END")
            self.mw_socket.close()

    def __init__(self, mw_endpoint, key_queue_endpoint, ventilator_endpoint, mappers_ready_endpoint):
        self.mw_endpoint = mw_endpoint
        self.key_queue_endpoint = key_queue_endpoint
        self.ventilator_endpoint = ventilator_endpoint
        self.mappers_ready_endpoint = mappers_ready_endpoint
        self.dispatcher_conn = self.ShotlogDispatcherConnection(self.ventilator_endpoint, self.mappers_ready_endpoint)
        self.reducer_handler_conn = self.ReducerHandlerConnection(self.key_queue_endpoint)
        self.pair_dispatcher_conn = self.PairDispatcherConnection(self.mw_endpoint)

    def receive_task(self):
        return self.dispatcher_conn.receive_task()

    def notify_key(self, key):
        self.reducer_handler_conn.notify_key(key)

    def send(self, data):
        self.pair_dispatcher_conn.send(data)

    def close(self):
        self.reducer_handler_conn.close()
        self.pair_dispatcher_conn.close()
        self.dispatcher_conn.close()
