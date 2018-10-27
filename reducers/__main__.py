import time
import logging

import zmq

from .reducer import Reducer

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")
logger = logging.getLogger("Reducers")

mw_endpoint = "tcp://0.0.0.0:5559"
key_queue_endpoint = "tcp://0.0.0.0:5560"
reducer_spawner_endpoint = "tcp://0.0.0.0:5561"

logger.debug("Start")

context = zmq.Context()

reducer_spawner_server = context.socket(zmq.REQ)
reducer_spawner_server.connect(reducer_spawner_endpoint)

server = context.socket(zmq.PULL)
server.bind(key_queue_endpoint)

logger.debug("Spawning reducers")
reducers = {}
while True:
    logger.debug("Receiving key from mapper")
    key = server.recv()
    logger.debug("Received key: %r", key)
    if key == b"END":
        logger.debug("END received")
        break
    elif key in reducers:
        logger.debug("A reducer is already created for key: %r", key)
    else:
        logger.debug("Starting new reducer")
        r = Reducer(key, mw_endpoint)
        r.start()
        reducers[key] = r

time.sleep(0.1)  # FIXME time for reducers to stabilize?? Otherwise first msgs are lost. Taken from zmq doc example
reducer_spawner_server.send(b"READY")

logger.debug("Joining reducers")
for key in reducers:
    logger.debug("Joining reducer with key %r", key)
    reducers[key].join()

logger.debug("End")
