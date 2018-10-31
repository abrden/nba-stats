FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /1_mw_bundle

RUN pip3 install zmq

COPY ./1_middleware /1_mw_bundle/1_middleware
COPY ./middleware /1_mw_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "1_middleware" ]
