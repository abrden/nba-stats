import os
import logging

from middleware.middleware import Middleware

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")

N = int(os.environ['MAPPERS'])  # Mappers quantity

endpoint = os.environ['ENDPOINT']
reducer_spawner_endpoint = os.environ['REDUCER_SPAWNER_ENDPOINT']


def main():
    logger = logging.getLogger("Middleware")
    logger.debug("Start")
    mw = Middleware(N, endpoint, reducer_spawner_endpoint)
    mw.start()
    logger.debug("End")


if __name__ == "__main__":
    main()
