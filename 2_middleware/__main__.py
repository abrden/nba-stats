import os
import logging

from middleware.middleware import Middleware

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")

N = int(os.environ['MAPPERS'])  # Mappers quantity

endpoint = "tcp://0.0.0.0:5559"
reducer_spawner_endpoint = "tcp://0.0.0.0:5561"


def main():
    logger = logging.getLogger("Middleware")
    logger.debug("Start")
    mw = Middleware(N, endpoint, reducer_spawner_endpoint)
    mw.start()
    logger.debug("End")


if __name__ == "__main__":
    main()
