import os
import logging

from reducer.reducer_spawner import ReducerSpawner

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")

N = int(os.environ['MAPPERS'])  # Mappers quantity

mw_endpoint = "tcp://0.0.0.0:5559"
key_queue_endpoint = "tcp://0.0.0.0:5560"
reducer_spawner_endpoint = "tcp://0.0.0.0:5561"
reducers_ready_endpoint = "tcp://0.0.0.0:5564"


def fun(acc, req):
    if acc is None:
        acc = 0
    return acc + 1


def main():
    logger = logging.getLogger("Reducers")
    logger.debug("Start")
    spawner = ReducerSpawner(key_queue_endpoint, reducer_spawner_endpoint, reducers_ready_endpoint)
    spawner.start(N, mw_endpoint, fun)
    spawner.close()
    logger.debug("End")


if __name__ == "__main__":
    main()
