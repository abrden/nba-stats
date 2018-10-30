FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /1_ventilator_bundle

RUN pip3 install zmq

COPY ./NBA-shot-log  /1_ventilator_bundle/NBA-shot-log
COPY ./1_ventilator /1_ventilator_bundle/1_ventilator
COPY ./ventilator /1_ventilator_bundle/ventilator

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "1_ventilator" ]
