import os
import logging

import zmq

from .reducer import Reducer

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")
logger = logging.getLogger("Reducers")

N = int(os.environ['MAPPERS'])  # Mappers quantity

mw_endpoint = "tcp://0.0.0.0:5559"
key_queue_endpoint = "tcp://0.0.0.0:5560"
reducer_spawner_endpoint = "tcp://0.0.0.0:5561"
reducers_ready_endpoint = "tcp://0.0.0.0:5564"

logger.debug("Start")

context = zmq.Context()

reducer_spawner_server = context.socket(zmq.REQ)
reducer_spawner_server.connect(reducer_spawner_endpoint)

reducers_ready_server = context.socket(zmq.PULL)
reducers_ready_server.bind(reducers_ready_endpoint)

key_server = context.socket(zmq.PULL)
key_server.bind(key_queue_endpoint)


logger.debug("Spawning reducers")
reducers = {}
ends_received = 0
while True:
    logger.debug("Receiving key from mapper")
    key = key_server.recv()
    logger.debug("Received key: %r", key)
    if key == b"END":
        logger.debug("END received")
        ends_received += 1
        if ends_received == N:
            break
    elif key in reducers:
        logger.debug("A reducer is already created for key: %r", key)
    else:
        logger.debug("Starting new reducer")
        r = Reducer(key, mw_endpoint, reducers_ready_endpoint)
        r.start()
        reducers[key] = r

logger.debug("Waiting for reducers ready ACK")
for key in reducers:
    ack = reducers_ready_server.recv()
    logger.debug("Reducer ACK received: %r", ack)
logger.debug("Sending overall ACK to MW")
reducer_spawner_server.send(b"READY")

logger.debug("Joining reducers")
for key in reducers:
    logger.debug("Joining reducer with key %r", key)
    reducers[key].join()

logger.debug("End")
