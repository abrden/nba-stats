import os
import logging
from multiprocessing import Pool

from sink.sink import DataSink

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")

endpoint = os.environ['ENDPOINT']
reducer_spawner_endpoint = os.environ['REDUCER_SPAWNER_ENDPOINT']
collector_endpoint = os.environ['COLLECTOR_ENDPOINT']


def format_result(result):
    teams, scores = result
    return teams[2:12], teams[16:19], scores[1], teams[23:26], scores[2]


def collect_fun(results):
    '''
    Takes a list of pairs ("(date, local_team, away_team)", {1: local_total, away_total}).
    Returns a list of tuples (date, local_team, local_total, away_team, away_total).
    '''
    logger = logging.getLogger("collect_fun")
    logger.debug("results %r", results)
    pool = Pool()
    decoded_results = pool.map(format_result, results)
    logger.debug("decoded results %r", decoded_results)
    return decoded_results


def main():
    logger = logging.getLogger("Sink")
    logger.debug("Start")
    sink = DataSink(endpoint, collector_endpoint)
    sink.start(reducer_spawner_endpoint, collect_fun)
    logger.debug("End")


if __name__ == "__main__":
    main()
