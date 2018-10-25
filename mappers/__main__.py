import logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")
logger = logging.getLogger("Mappers")

from .mapper import Mapper

logger.debug("Start")

endpoint = "tcp://0.0.0.0:5559"
data = list(range(1, 11))

mapper = Mapper(endpoint, data)
mapper.start()
mapper.join()

logger.debug("End")
