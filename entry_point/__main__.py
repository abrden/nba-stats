import logging

from .trigger import Trigger
from .results_collector import ResultsCollector

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")

ventilator_endpoint_1 = "tcp://0.0.0.0:5570"
ventilator_endpoint_2 = "tcp://0.0.0.0:5571"
ventilator_endpoint_3 = "tcp://0.0.0.0:5572"

endpoint = "tcp://0.0.0.0:5573"


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
