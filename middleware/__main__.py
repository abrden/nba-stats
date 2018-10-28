import logging

import zmq

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")
logger = logging.getLogger("Middleware")

endpoint = "tcp://0.0.0.0:5559"
reducer_spawner_endpoint = "tcp://0.0.0.0:5561"

logger.debug("Start")
context = zmq.Context()
server = context.socket(zmq.ROUTER)
server.bind(endpoint)

reducer_spawner_client = context.socket(zmq.REP)
reducer_spawner_client.bind(reducer_spawner_endpoint)

logger.debug("Waiting for reducer spawner signal")
reducer_spawner_client.recv()
logger.debug("Signal received, sending data to reducers")

keys = {}
while True:
    logger.debug("Receiving message from mappers")
    message = server.recv_multipart()  # FIXME why do I have to recv a multipart if mapper sent me a string
    logger.debug("Multipart received %r", message)
    if message[3] == b"END":
        logger.debug("END received")
        break
    key, value = message[3].split('#'.encode())

    if key not in keys:
        keys[key] = True

    logger.debug("Message received %r, key %r, value %r", message[3], key, value)
    logger.debug("Sending message to reducer")
    server.send_multipart([key, value])
    logger.debug("Task sent")

logger.debug("Sending END to reducers")
for key in keys:
    server.send_multipart([key, b'END'])
logger.debug("End")

