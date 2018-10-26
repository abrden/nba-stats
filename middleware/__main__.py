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
    key, value = message.split('#'.encode())
    logger.debug("Message received %r, key %r, value %r", message, key, value)
    logger.debug("Sending message to reducer")
    client.send_multipart([key, value])
    logger.debug("Task sent")

client.send_multipart([b'A', b'END'])  # FIXME implement for dynamic keys
client.send_multipart([b'B', b'END'])
logger.debug("End")
