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
    Takes a row of a shot log. Returns None if the shot is MISSED, or a pair
    ((date, local_team, away_team, index_of_team_that_scored), points_scored) if the shot is SCORED.
    '''

    return "du", "mmy"


def main():
    logger = logging.getLogger("Mapper")
    logger.debug("Start")
    mapper = Mapper(mw_endpoint, key_queue_endpoint, ventilator_endpoint, mappers_ready_endpoint)
    mapper.start(map_fun)
    logger.debug("End")


if __name__ == "__main__":
    main()
