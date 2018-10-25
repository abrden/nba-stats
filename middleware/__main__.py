import time
import random
import logging

import zmq

from middleware.reducer import Reducer

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")
logger = logging.getLogger("Main")

endpoint = "tcp://0.0.0.0:5559"

logger.debug("Start")
context = zmq.Context()
client = context.socket(zmq.ROUTER)
client.bind(endpoint)

logger.debug("Starting reducers")
Reducer(b'A', endpoint).start()  # FIXME spawn reducers from another process
Reducer(b'B', endpoint).start()

logger.debug("Sleeping")
# Wait for threads to stabilize
time.sleep(1)  # FIXME whyy??

# Send 10 tasks scattered to A twice as often as B
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
