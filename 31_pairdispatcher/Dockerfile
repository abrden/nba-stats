FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /31_pairdispatcher_bundle

RUN pip3 install zmq

COPY ./31_pairdispatcher /31_pairdispatcher_bundle/31_pairdispatcher
COPY ./pair_dispatcher /31_pairdispatcher_bundle/pair_dispatcher
COPY ./middleware /31_pairdispatcher_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "31_pairdispatcher" ]
