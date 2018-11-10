FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /32_mw_bundle

RUN pip3 install zmq

COPY ./32_middleware /32_mw_bundle/32_middleware
COPY ./middleware /32_mw_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "32_middleware" ]
