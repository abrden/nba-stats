FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /31_shotlogdispatcher_bundle

RUN pip3 install zmq

COPY ./31_shotlogdispatcher /31_shotlogdispatcher_bundle/31_shotlogdispatcher
COPY ./shotlog_dispatcher /31_shotlogdispatcher_bundle/shotlog_dispatcher

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "31_shotlogdispatcher" ]
