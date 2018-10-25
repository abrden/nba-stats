import logging

import zmq

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")
logger = logging.getLogger("Mappers")

endpoint = "tcp://0.0.0.0:5559"

logger.debug("Start")
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.setsockopt(zmq.REQ_RELAXED, 1)
socket.setsockopt(zmq.REQ_CORRELATE, 1)
socket.connect(endpoint)

# Send 10 tasks
for i in range(10):
    logger.debug("Sending message to MW")
    socket.send("hello world {}".format(i).encode())
    logger.debug("Task sent to MW")

socket.send(b'END')
logger.debug("End")
