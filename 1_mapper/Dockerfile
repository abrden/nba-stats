FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /1_mapper_bundle

RUN pip3 install zmq

COPY ./1_mapper /1_mapper_bundle/1_mapper
COPY ./mapper /1_mapper_bundle/mapper
COPY ./middleware /1_mapper_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "1_mapper" ]
