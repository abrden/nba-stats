import logging

from .mapper import Mapper

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")
logger = logging.getLogger("Mappers")

logger.debug("Start")

mw_endpoint = "tcp://0.0.0.0:5559"
key_queue_endpoint = "tcp://0.0.0.0:5560"
ventilator_endpoint = "tcp://0.0.0.0:5562"
mappers_ready_endpoint = "tcp://0.0.0.0:5563"

mapper = Mapper(mw_endpoint, key_queue_endpoint, ventilator_endpoint,
                mappers_ready_endpoint)
mapper.start()
mapper.join()

logger.debug("End")
