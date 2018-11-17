FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /2_reducer_bundle

RUN pip3 install zmq

COPY ./2_reducer /2_reducer_bundle/2_reducer
COPY ./reducer /2_reducer_bundle/reducer
COPY ./middleware /2_reducer_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "2_reducer" ]
