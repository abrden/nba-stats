import logging

from mapper.mapper import Mapper

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")

mw_endpoint = "tcp://0.0.0.0:5559"
key_queue_endpoint = "tcp://0.0.0.0:5560"
ventilator_endpoint = "tcp://0.0.0.0:5562"
mappers_ready_endpoint = "tcp://0.0.0.0:5563"


def map_fun(task):
    '''
    Takes a row of a shot log. Returns None if the shot is MISSED, or a pair (player_name, points) if the shot is SCORED.
    '''

    SHOT_OUTCOME_INDEX = 15
    SHOT_PLAYER_INDEX = 12
    POINTS_INDEX = 7

    shot_log = task.decode().rstrip().split(",")
    if shot_log[SHOT_OUTCOME_INDEX] == "SCORED":
        return shot_log[SHOT_PLAYER_INDEX], shot_log[POINTS_INDEX]


def main():
    logger = logging.getLogger("Mapper")
    logger.debug("Start")
    mapper = Mapper(mw_endpoint, key_queue_endpoint, ventilator_endpoint, mappers_ready_endpoint)
    mapper.start(map_fun)
    logger.debug("End")


if __name__ == "__main__":
    main()
