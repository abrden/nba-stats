import os
import logging

from .trigger import Trigger
from .results_collector import ResultsCollector

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")

ventilator_endpoint_1 = os.environ['VENT1_ENDPOINT']
ventilator_endpoint_2 = os.environ['VENT2_ENDPOINT']
ventilator_endpoint_3 = os.environ['VENT3_ENDPOINT']

endpoint = os.environ['ENDPOINT']


def main():
    logger = logging.getLogger("EntryPoint")
    logger.debug("Start")
    t = Trigger(ventilator_endpoint_1, ventilator_endpoint_2, ventilator_endpoint_3)
    t.start()
    logger.debug("Collecting results")
    c = ResultsCollector(endpoint)
    results = c.start()
    logger.debug("The results are: %r", results)
    logger.debug("End")


if __name__ == "__main__":
    main()
