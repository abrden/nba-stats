FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /1_reducerspawner_bundle

RUN pip3 install zmq

COPY ./1_reducerspawner /1_reducerspawner_bundle/1_reducerspawner
COPY ./reducer /1_reducerspawner_bundle/reducer

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "1_reducerspawner" ]
