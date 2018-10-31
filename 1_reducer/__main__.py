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
    Takes the accumulated scored points of the teams and the new points scored by a team.
    Returns the accumulated points of the team.
    '''
    points = req  # Tuple (team_index, new_points)
    if acc is None:
        acc = {1: 0, 2: 0}

    acc[points[0]] += points[1]
    return acc


def main():
    logger = logging.getLogger("Reducers")
    logger.debug("Start")
    spawner = ReducerSpawner(key_queue_endpoint, reducer_spawner_endpoint, reducers_ready_endpoint, spawner_sink_endpoint)
    spawner.start(N, mw_endpoint, reducer_reducers_ready_endpoint, reducer_sink_endpoint, fun)
    spawner.close()
    logger.debug("End")


if __name__ == "__main__":
    main()
