FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /2_pairdispatcher_bundle

RUN pip3 install zmq

COPY ./2_pairdispatcher /2_pairdispatcher_bundle/2_pairdispatcher
COPY ./pair_dispatcher /2_pairdispatcher_bundle/pair_dispatcher
COPY ./middleware /2_pairdispatcher_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "2_pairdispatcher" ]
