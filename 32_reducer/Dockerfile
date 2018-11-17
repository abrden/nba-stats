FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /32_reducer_bundle

RUN pip3 install zmq

COPY ./32_reducer /32_reducer_bundle/32_reducer
COPY ./reducer /32_reducer_bundle/reducer
COPY ./middleware /32_reducer_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "32_reducer" ]
