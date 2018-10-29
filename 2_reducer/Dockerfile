FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /2_mw_bundle

RUN pip3 install pyzmq

COPY ./2_middleware /2_mw_bundle/2_middleware
COPY ./middleware /2_mw_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-m", "2_middleware" ]
