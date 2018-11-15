FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /31_reducerhandler_bundle

RUN pip3 install zmq

COPY ./31_reducerhandler /31_reducerhandler_bundle/31_reducerhandler
COPY ./reducer_handler /31_reducerhandler_bundle/reducer_handler
COPY ./middleware /31_reducerhandler_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "31_reducerhandler" ]
