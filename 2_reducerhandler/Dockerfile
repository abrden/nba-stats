FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /2_reducerhandler_bundle

RUN pip3 install zmq

COPY ./2_reducerhandler /2_reducerhandler_bundle/2_reducerhandler
COPY ./reducer_handler /2_reducerhandler_bundle/reducer_handler

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "2_reducerhandler" ]
