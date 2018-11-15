FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /1_sink_bundle

RUN pip3 install zmq

COPY ./1_sink /1_sink_bundle/1_sink
COPY ./sink /1_sink_bundle/sink
COPY ./middleware /1_sink_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "1_sink" ]
