import os
import logging

from mapper.mapper import Mapper

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")

mw_endpoint = os.environ['MW_ENDPOINT']
key_queue_endpoint = os.environ['KEYS_ENDPOINT']
ventilator_endpoint = os.environ['VENTILATOR_ENDPOINT']
mappers_ready_endpoint = os.environ['MAPPERS_READY_ENDPOINT']


def map_fun(task):
    '''
    Takes a str containing a tuple (date, local_team, local_score, away_team, away_score).
    Returns a tuple (local_team, local_win) with local_win being a boolean True if the local team won, False if loose or tied.
    '''
    tuple = task.decode()
    local_team = tuple[16:19]
    local_score = int(tuple.split(', ')[2])
    away_score = int(tuple.split(', ')[4][:-1])
    local_win = False
    if local_score - away_score > 0:  # Tied games are considered a loss
        local_win = True
    return local_team, local_win


def main():
    logger = logging.getLogger("Mapper")
    logger.debug("Start")
    mapper = Mapper(mw_endpoint, key_queue_endpoint, ventilator_endpoint, mappers_ready_endpoint)
    mapper.start(map_fun)
    logger.debug("End")


if __name__ == "__main__":
    main()
