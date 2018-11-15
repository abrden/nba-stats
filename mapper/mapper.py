import logging

from middleware.mapper import MapperMiddleware


class Mapper:

    def __init__(self, mw_endpoint, key_queue_endpoint, ventilator_endpoint, mappers_ready_endpoint):
        self.logger = logging.getLogger("Mapper")
        self.mw_endpoint = mw_endpoint
        self.key_queue_endpoint = key_queue_endpoint
        self.ventilator_endpoint = ventilator_endpoint
        self.mappers_ready_endpoint = mappers_ready_endpoint
        self.conn = None

    def start(self, fun):
        self.conn = MapperMiddleware(self.mw_endpoint, self.key_queue_endpoint, self.ventilator_endpoint, self.mappers_ready_endpoint)

        while True:
            self.logger.debug("Waiting for task from shotlog_dispatcher")
            task = self.conn.receive_task()
            if task == b"END":
                self.logger.debug("END received")
                self.conn.notify_key("END")  # TODO Implement close method for conn objects
                self.conn.send(b"END")
                return
            self.logger.debug("Task received: %s", task)

            result = fun(task)
            if result:
                key, value = result
                self.logger.debug("Emitting result: (%s, %s)", key, value)
                self.conn.notify_key(key)
                self.conn.send(result)
            else:
                self.logger.debug("Result is None. Not emitting.")
