FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /1_pairdispatcher_bundle

RUN pip3 install zmq

COPY ./1_pairdispatcher /1_pairdispatcher_bundle/1_pairdispatcher
COPY ./pair_dispatcher /1_pairdispatcher_bundle/pair_dispatcher
COPY ./middleware /1_pairdispatcher_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "1_pairdispatcher" ]
