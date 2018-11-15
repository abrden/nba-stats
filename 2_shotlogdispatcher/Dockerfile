FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /2_shotlogdispatcher_bundle

RUN pip3 install zmq

COPY ./2_shotlogdispatcher /2_shotlogdispatcher_bundle/2_shotlogdispatcher
COPY ./shotlog_dispatcher /2_shotlogdispatcher_bundle/shotlog_dispatcher
COPY ./middleware /2_shotlogdispatcher_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "2_shotlogdispatcher" ]
