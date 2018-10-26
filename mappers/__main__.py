import logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")
logger = logging.getLogger("Mappers")

from .mapper import Mapper

logger.debug("Start")

mw_endpoint = "tcp://0.0.0.0:5559"
key_queue_endpoint = "tcp://0.0.0.0:5560"
data = list(range(1, 11))

mapper = Mapper(mw_endpoint, key_queue_endpoint, data)
mapper.start()
mapper.join()

logger.debug("End")
