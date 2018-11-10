import os
import logging

from .reducer_spawner import ReducerSpawner

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")

mappers = int(os.environ['MAPPERS'])
reducers = int(os.environ['REDUCERS'])

key_queue_endpoint = os.environ['KEY_QUEUE_ENDPOINT']
keys_to_reducers_endpoint = os.environ['KEYS_REDUCERS_ENDPOINT']
reducers_ready_endpoint = os.environ['REDUCERS_READY_ENDPOINT']
spawner_sink_endpoint = os.environ['SPAWNER_SINK_ENDPOINT']


def main():
    logger = logging.getLogger("ReducerSpawner")
    logger.debug("Start")
    spawner = ReducerSpawner(mappers, reducers, key_queue_endpoint, keys_to_reducers_endpoint, reducers_ready_endpoint, spawner_sink_endpoint)
    spawner.start()
    logger.debug("End")


if __name__ == "__main__":
    main()
