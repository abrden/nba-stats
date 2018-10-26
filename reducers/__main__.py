import logging

import zmq

from reducers.reducer import Reducer

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")
logger = logging.getLogger("Reducers")

mw_endpoint = "tcp://0.0.0.0:5559"
key_queue_endpoint = "tcp://0.0.0.0:5560"

logger.debug("Start")

context = zmq.Context()
server = context.socket(zmq.PULL)
#server.setsockopt(zmq.REQ_RELAXED, 1)
#server.setsockopt(zmq.REQ_CORRELATE, 1)
server.bind(key_queue_endpoint)

reducers = {}
for _ in range(10):
    logger.debug("Receiving key from mappers")
    key = server.recv()
    logger.debug("Received key: %r", key)
    if key in reducers:
        logger.debug("A reducer is already created for key: %r", key)
    else:
        logger.debug("Starting new reducer")
        r = Reducer(key, mw_endpoint)
        r.start()  # FIXME join reducers
        reducers[key] = r

logger.debug("End")
