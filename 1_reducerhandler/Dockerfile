FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /1_reducerhandler_bundle

RUN pip3 install zmq

COPY ./1_reducerhandler /1_reducerhandler_bundle/1_reducerhandler
COPY ./reducer_handler /1_reducerhandler_bundle/reducer_handler

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "1_reducerhandler" ]
