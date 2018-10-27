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

for _ in range(10):
    logger.debug("Receiving message from mappers")
    message = server.recv_multipart()  # FIXME why
    logger.debug("Multipart received %r", message)
    key, value = message[3].split('#'.encode())  # FIXME WHYYYY
    logger.debug("Message received %r, key %r, value %r", message[3], key, value)
    logger.debug("Sending message to reducer")
    server.send_multipart([key, value])
    logger.debug("Task sent")

server.send_multipart([b'A', b'END'])  # FIXME implement for dynamic keys
server.send_multipart([b'B', b'END'])
logger.debug("End")

