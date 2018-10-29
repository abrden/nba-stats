import os
import logging

from .data_ventilator import DataVentilator

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")

N = int(os.environ['MAPPERS'])  # Mappers quantity
DATASET_DIR = os.environ['DATASET_DIR']

entry_signal_endpoint = "tcp://0.0.0.0:5571"
ventilator_endpoint = "tcp://0.0.0.0:5562"
mappers_ready_endpoint = "tcp://0.0.0.0:5563"


def main():
    logger = logging.getLogger("Ventilator")
    logger.debug("Start")
    ventilator = DataVentilator(N, ventilator_endpoint, mappers_ready_endpoint, entry_signal_endpoint)
    ventilator.start(DATASET_DIR)
    logger.debug("End")


if __name__ == "__main__":
    main()
