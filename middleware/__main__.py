import random
import logging

import zmq

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")
logger = logging.getLogger("Middleware")

endpoint = "tcp://0.0.0.0:5559"

logger.debug("Start")
context = zmq.Context()
client = context.socket(zmq.ROUTER)
client.bind(endpoint)

for _ in range(10):
    logger.debug("Receiving message from mappers")
    message = client.recv()
    logger.debug("Message received %r", message)
    ident = random.choice([b'A', b'B'])
    logger.debug("Sending message to reducer")
    client.send_multipart([ident, message])
    logger.debug("Task sent")

client.send_multipart([b'A', b'END'])
client.send_multipart([b'B', b'END'])
logger.debug("End")
