FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /32_sink_bundle

RUN pip3 install zmq

COPY ./32_sink /32_sink_bundle/32_sink
COPY ./sink /32_sink_bundle/sink
COPY ./middleware /32_sink_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "32_sink" ]
