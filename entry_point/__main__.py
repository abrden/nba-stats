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
    c = ResultsCollector(endpoint)
    results = c.start()
    logger.debug("\nPuntaje final para cada partido:\n%r\nLos 10 mejores goleadores:\n%r\nEstadisticas sobre el equipo local (tiros acertados):\n%r\n",
                 results[1],
                 results[2],
                 results[32])
    logger.debug("End")


if __name__ == "__main__":
    main()
