import os
import logging

from ventilator.data_ventilator import DataVentilator

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")

N = int(os.environ['MAPPERS'])  # Mappers quantity
DATASET_DIR = os.environ['DATASET_DIR']

entry_signal_endpoint = os.environ["ENTRY_ENDPOINT"]
ventilator_endpoint = os.environ["ENDPOINT"]
mappers_ready_endpoint = os.environ["MAPPERS_READY_ENDPOINT"]


def main():
    logger = logging.getLogger("Ventilator")
    logger.debug("Start")
    ventilator = DataVentilator(N, ventilator_endpoint, mappers_ready_endpoint, entry_signal_endpoint)
    ventilator.start(DATASET_DIR)
    logger.debug("End")


if __name__ == "__main__":
    main()
