FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /1_shotlogdispatcher_bundle

RUN pip3 install zmq

COPY ./1_shotlogdispatcher /1_shotlogdispatcher_bundle/1_shotlogdispatcher
COPY ./shotlog_dispatcher /1_shotlogdispatcher_bundle/shotlog_dispatcher

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "1_shotlogdispatcher" ]
