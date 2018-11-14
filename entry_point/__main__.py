import os
import logging

from .data_ventilator import DataVentilator
from .results_collector import ResultsCollector

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")

ventilator_endpoint_1 = os.environ['VENT1_ENDPOINT']
ventilator_endpoint_2 = os.environ['VENT2_ENDPOINT']
ventilator_endpoint_3 = os.environ['VENT3_ENDPOINT']
dataset_dir = os.environ['DATASET_DIR']
endpoint = os.environ['ENDPOINT']
dispatcher_ready_endpoint = os.environ["DISPATCHER_READY_ENDPOINT"]

def main():
    logger = logging.getLogger("EntryPoint")
    logger.debug("Start")
    v = DataVentilator(ventilator_endpoint_1, ventilator_endpoint_2, ventilator_endpoint_3, dispatcher_ready_endpoint, dataset_dir)
    v.start()
    c = ResultsCollector(endpoint)
    results = c.start()
    logger.debug("The results are: %r", results)
    logger.debug("End")


if __name__ == "__main__":
    main()
