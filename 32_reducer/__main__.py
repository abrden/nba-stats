import os
import logging

from .reducer import Reducer

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")

mw_endpoint = os.environ['MW_ENDPOINT']
reducer_mw_ready_endpoint = os.environ['REDUCER_MW_READY_ENDPOINT']
reducer_handler_ready_endpoint = os.environ['REDUCER_HANDLER_READY_ENDPOINT']
sink_endpoint = os.environ['SINK_ENDPOINT']
keys_endpoint = os.environ['KEYS_ENDPOINT']


def fun(acc, req):
    '''
    Takes the accumulated shots scored and the shots total, and a tuple (points, scored_bool)
    '''
    POINTS_INDEX = 0
    SCORED_INDEX = 1
    if acc is None:
        acc = {2: (0, 0), 3: (0, 0)}

    scored_points = acc[req[POINTS_INDEX]][0]
    if req[SCORED_INDEX]:
        scored_points += 1

    acc[req[POINTS_INDEX]] = (scored_points, acc[req[POINTS_INDEX]][1] + 1)
    return acc


def main():
    logger = logging.getLogger("Reducer")
    logger.debug("Start")
    r = Reducer(mw_endpoint, reducer_mw_ready_endpoint, keys_endpoint, reducer_handler_ready_endpoint, sink_endpoint)
    r.start(fun)
    logger.debug("End")


if __name__ == "__main__":
    main()
