FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /2_ventilator_bundle

RUN pip3 install zmq

COPY ./NBA-shot-log  /2_ventilator_bundle/NBA-shot-log
COPY ./ventilator /2_ventilator_bundle/2_ventilator

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "2_ventilator" ]
