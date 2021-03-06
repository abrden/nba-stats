import os
import logging

from reducer.reducer import Reducer

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")

mw_endpoint = os.environ['MW_ENDPOINT']
reducer_mw_ready_endpoint = os.environ['REDUCER_MW_READY_ENDPOINT']
reducer_handler_ready_endpoint = os.environ['REDUCER_HANDLER_READY_ENDPOINT']
sink_endpoint = os.environ['SINK_ENDPOINT']
keys_endpoint = os.environ['KEYS_ENDPOINT']


def fun(acc, req):
    '''
    Takes the accumulated scored points of the player and the new points. Returns the sum of the accumulated and the new points.
    '''
    points = int(req)
    if acc is None:
        acc = 0
    return acc + points


def main():
    logger = logging.getLogger("Reducer")
    logger.debug("Start")
    r = Reducer(mw_endpoint, reducer_mw_ready_endpoint, keys_endpoint, reducer_handler_ready_endpoint, sink_endpoint)
    r.start(fun)
    logger.debug("End")


if __name__ == "__main__":
    main()
