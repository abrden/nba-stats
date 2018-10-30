import os
import logging

from reducer.reducer_spawner import ReducerSpawner

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")

N = int(os.environ['MAPPERS'])  # Mappers quantity

mw_endpoint = os.environ['MW_ENDPOINT']
key_queue_endpoint = os.environ['KEY_QUEUE_ENDPOINT']
reducer_spawner_endpoint = os.environ['REDUCER_SPAWNER_ENDPOINT']
reducers_ready_endpoint = os.environ['REDUCERS_READY_ENDPOINT']
reducer_reducers_ready_endpoint = os.environ['REDUCER_REDUCERS_READY_ENDPOINT']
reducer_sink_endpoint = os.environ['REDUCER_SINK_ENDPOINT']
spawner_sink_endpoint = os.environ['SPAWNER_SINK_ENDPOINT']


def fun(acc, req):
    '''
    Takes the accumulated scored points of the player and the new points. Returns the sum of the accumulated and the new points.
    '''
    points = int(req.decode())
    if acc is None:
        acc = 0
    return acc + points


def main():
    logger = logging.getLogger("Reducers")
    logger.debug("Start")
    spawner = ReducerSpawner(key_queue_endpoint, reducer_spawner_endpoint, reducers_ready_endpoint, spawner_sink_endpoint)
    spawner.start(N, mw_endpoint, reducer_reducers_ready_endpoint, reducer_sink_endpoint, fun)
    spawner.close()
    logger.debug("End")


if __name__ == "__main__":
    main()
