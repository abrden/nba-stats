import os
import logging

from shotlog_dispatcher.data_dispatcher import DataDispatcher

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")

N = int(os.environ['MAPPERS'])  # Mappers quantity

entry_signal_endpoint = os.environ["ENTRY_ENDPOINT"]
ventilator_endpoint = os.environ["ENDPOINT"]
mappers_ready_endpoint = os.environ["MAPPERS_READY_ENDPOINT"]
dispatcher_ready_endpoint = os.environ["DISPATCHER_READY_ENDPOINT"]

def main():
    logger = logging.getLogger("Ventilator")
    logger.debug("Start")
    d = DataDispatcher(N, ventilator_endpoint, dispatcher_ready_endpoint, mappers_ready_endpoint, entry_signal_endpoint)
    d.start()
    logger.debug("End")


if __name__ == "__main__":
    main()
