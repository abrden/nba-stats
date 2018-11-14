FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /31_mw_bundle

RUN pip3 install zmq

COPY ./31_middleware /31_mw_bundle/31_middleware
COPY ./middleware /31_mw_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "31_middleware" ]
