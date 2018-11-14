FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /31_mapper_bundle

RUN pip3 install zmq

COPY ./31_mapper /31_mapper_bundle/31_mapper
COPY ./mapper /31_mapper_bundle/mapper

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "31_mapper" ]
