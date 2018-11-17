FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /32_shotlogdispatcher_bundle

RUN pip3 install zmq

COPY ./32_shotlogdispatcher /32_shotlogdispatcher_bundle/32_shotlogdispatcher
COPY ./shotlog_dispatcher /32_shotlogdispatcher_bundle/shotlog_dispatcher
COPY ./middleware /32_shotlogdispatcher_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "32_shotlogdispatcher" ]
