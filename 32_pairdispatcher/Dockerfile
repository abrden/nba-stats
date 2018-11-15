FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /32_pairdispatcher_bundle

RUN pip3 install zmq

COPY ./32_pairdispatcher /32_pairdispatcher_bundle/32_pairdispatcher
COPY ./pair_dispatcher /32_pairdispatcher_bundle/pair_dispatcher
COPY ./middleware /32_pairdispatcher_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "32_pairdispatcher" ]
