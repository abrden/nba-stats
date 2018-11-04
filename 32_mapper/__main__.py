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
    Takes a row of a shot log. Returns None if the shot is from the away team, or a pair
    (local_team, (points_scored, scored_bool)) if the shot is from the local team.
    '''

    SHOT_OUTCOME_INDEX = 15
    LOCAL_TEAM_INDEX = 5
    POINTS_INDEX = 7
    HOME_TEAM_INDEX = 2

    shot_log = task.decode().rstrip().split(",")
    if shot_log[HOME_TEAM_INDEX] == "Yes":
        scored = False
        if shot_log[SHOT_OUTCOME_INDEX] == "SCORED":
            scored = True
        return shot_log[LOCAL_TEAM_INDEX], (int(shot_log[POINTS_INDEX]), scored)


def main():
    logger = logging.getLogger("Mapper")
    logger.debug("Start")
    mapper = Mapper(mw_endpoint, key_queue_endpoint, ventilator_endpoint, mappers_ready_endpoint)
    mapper.start(map_fun)
    logger.debug("End")


if __name__ == "__main__":
    main()
