import os
import logging

import zmq

from .dataset_handler import DatasetHandler

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")
logger = logging.getLogger("Ventilator")

# Takes N and dir of dataset
# Partitions all data in N and sends one partition to each mapper

N = int(os.environ['MAPPERS'])  # Mappers quantity
DATASET_DIR = os.environ['DATASET_DIR']

ventilator_endpoint = "tcp://0.0.0.0:5562"
mappers_ready_endpoint = "tcp://0.0.0.0:5563"

logger.debug("Start")
context = zmq.Context()

sender = context.socket(zmq.PUSH)
sender.bind(ventilator_endpoint)

mappers_ready_ack = context.socket(zmq.PULL)
mappers_ready_ack.bind(mappers_ready_endpoint)

logger.debug("Waiting for mappers ready ACK")
for _ in range(N):
    ack = mappers_ready_ack.recv()
    logger.debug("Mapper ACK received: %r", ack)


logger.debug("Sending data to mappers")
set_handler = DatasetHandler(DATASET_DIR)

shotlogs = set_handler.get_shotlogs()
for log in shotlogs:
    logger.debug("Reading shotlog: %s", log)
    with open(log, "r") as file:
        line = file.readline()
        while line:
            logger.debug("Read line: %s", line)
            sender.send_string(line)
            line = file.readline()

for _ in range(N):
    sender.send_string("END")

logger.debug("End")
