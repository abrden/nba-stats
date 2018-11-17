FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /2_sink_bundle

RUN pip3 install zmq

COPY ./2_sink /2_sink_bundle/2_sink
COPY ./sink /2_sink_bundle/sink
COPY ./middleware /2_sink_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "2_sink" ]
