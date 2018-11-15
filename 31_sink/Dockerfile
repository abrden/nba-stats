FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /31_sink_bundle

RUN pip3 install zmq

COPY ./31_sink /31_sink_bundle/31_sink
COPY ./sink /31_sink_bundle/sink
COPY ./middleware /31_sink_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "31_sink" ]
