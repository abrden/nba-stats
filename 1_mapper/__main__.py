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

    SHOT_OUTCOME_INDEX = 15
    DATE_INDEX = 11
    LOCAL_TEAM_INDEX = 5
    AWAY_TEAM_INDEX = 8
    POINTS_INDEX = 7
    HOME_TEAM_INDEX = 2

    shot_log = task.decode().rstrip().split(",")
    if shot_log[SHOT_OUTCOME_INDEX] == "SCORED":

        index_of_team_that_scored = 0  # ans tuple index of the team that scored (Starting at 1 bc date is at index 0)
        if shot_log[HOME_TEAM_INDEX] == 'Yes':
            index_of_team_that_scored = 1
        elif shot_log[HOME_TEAM_INDEX] == 'No':
            index_of_team_that_scored = 2
        else:
            return None

        ans = (shot_log[DATE_INDEX], shot_log[LOCAL_TEAM_INDEX], shot_log[AWAY_TEAM_INDEX]), (index_of_team_that_scored, int(shot_log[POINTS_INDEX]))
        key, value = ans
        return key, value


def main():
    logger = logging.getLogger("Mapper")
    logger.debug("Start")
    mapper = Mapper(mw_endpoint, key_queue_endpoint, ventilator_endpoint, mappers_ready_endpoint)
    mapper.start(map_fun)
    logger.debug("End")


if __name__ == "__main__":
    main()
