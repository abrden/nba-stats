FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /2_reducerspawner_bundle

RUN pip3 install zmq

COPY ./2_reducerspawner /2_reducerspawner_bundle/2_reducerspawner
COPY ./reducer_spawner /2_reducerspawner_bundle/reducer_spawner

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "2_reducerspawner" ]
