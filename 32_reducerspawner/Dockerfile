FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /32_reducerspawner_bundle

RUN pip3 install zmq

COPY ./32_reducerspawner /32_reducerspawner_bundle/32_reducerspawner
COPY ./reducer /32_reducerspawner_bundle/reducer

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "32_reducerspawner" ]
