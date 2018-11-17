FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /1_reducer_bundle

RUN pip3 install zmq

COPY ./1_reducer /1_reducer_bundle/1_reducer
COPY ./reducer /1_reducer_bundle/reducer
COPY ./middleware /1_reducer_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "1_reducer" ]
