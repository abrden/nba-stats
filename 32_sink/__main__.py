import os
import logging
from multiprocessing import Pool

from sink.sink import DataSink

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")

endpoint = os.environ['ENDPOINT']
reducer_spawner_endpoint = os.environ['REDUCER_SPAWNER_ENDPOINT']
collector_endpoint = os.environ['COLLECTOR_ENDPOINT']


def format_result(result):
    if result[1][2][1] > 0:
        tuple_2 = (result[0], 2, result[1][2][0]*100/result[1][2][1])
    else:
        tuple_2 = (result[0], 2, 0)

    if result[1][3][1] > 0:
        tuple_3 = (result[0], 3, result[1][3][0]*100/result[1][3][1])
    else:
        tuple_3 = (result[0], 3, 0)

    return tuple_2, tuple_3


def collect_fun(results):
    '''
    Takes a list of pairs (local_team, {2: (2s_scored, 2s_shots), 3: (3s_scored, 3s_shots)}).
    Returns a list of pairs (local_team, 2, %2_scored), (local_team, 3, %3_scored)
    '''

    pool = Pool()
    formatted_results = pool.map(format_result, results)
    pool.close()
    pool.join()
    return formatted_results


def main():
    logger = logging.getLogger("Sink")
    logger.debug("Start")
    sink = DataSink(endpoint, collector_endpoint, reducer_spawner_endpoint)
    sink.start(collect_fun)
    logger.debug("End")


if __name__ == "__main__":
    main()
