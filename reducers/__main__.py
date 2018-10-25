import logging

from reducers.reducer import Reducer

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")
logger = logging.getLogger("Reducers")

endpoint = "tcp://0.0.0.0:5559"

logger.debug("Start")

logger.debug("Starting reducers")
Reducer(b'A', endpoint).start()  # FIXME spawn reducers from another process
Reducer(b'B', endpoint).start()

logger.debug("End")
