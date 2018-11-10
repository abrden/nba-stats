import os
import logging

from middleware.middleware import Middleware

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")

mappers = int(os.environ['MAPPERS'])
reducers = int(os.environ['REDUCERS'])
endpoint = os.environ['ENDPOINT']
reducer_ready_endpoint = os.environ['REDUCER_READY_ENDPOINT']


def main():
    logger = logging.getLogger("Middleware")
    logger.debug("Start")
    mw = Middleware(mappers, reducers, endpoint, reducer_ready_endpoint)
    mw.start()
    logger.debug("End")


if __name__ == "__main__":
    main()
