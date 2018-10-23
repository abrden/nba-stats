import time
import random
import logging

import zmq

from reducer import Reducer

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")
logger = logging.getLogger("Main")

endpoint = "ipc://routing.ipc"

logger.debug("Start")
context = zmq.Context()
client = context.socket(zmq.ROUTER)
client.bind(endpoint)

logger.debug("Starting reducers")
Reducer(b'A', endpoint).start()
Reducer(b'B', endpoint).start()

logger.debug("Sleeping")
# Wait for threads to stabilize
time.sleep(1)  # FIXME whyy??

logger.debug("Sending tasks")
# Send 10 tasks scattered to A twice as often as B
for _ in range(10):
    # Send two message parts, first the address…
    ident = random.choice([b'A', b'A', b'B'])
    # And then the workload
    work = b"This is the workload"
    client.send_multipart([ident, work])
    logger.debug("Task sent")

client.send_multipart([b'A', b'END'])
client.send_multipart([b'B', b'END'])
logger.debug("End")
