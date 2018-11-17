FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /32_reducerhandler_bundle

RUN pip3 install zmq

COPY ./32_reducerhandler /32_reducerhandler_bundle/32_reducerhandler
COPY ./reducer_handler /32_reducerhandler_bundle/reducer_handler
COPY ./middleware /32_reducerhandler_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "32_reducerhandler" ]
