FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /31_reducer_bundle

RUN pip3 install zmq

COPY ./31_reducer /31_reducer_bundle/31_reducer
COPY ./reducer /31_reducer_bundle/reducer

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "31_reducer" ]
