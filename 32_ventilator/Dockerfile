FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /32_ventilator_bundle

RUN pip3 install zmq

COPY ./NBA-shot-log  /32_ventilator_bundle/NBA-shot-log
COPY ./32_ventilator /32_ventilator_bundle/32_ventilator
COPY ./ventilator /32_ventilator_bundle/ventilator

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "32_ventilator" ]
