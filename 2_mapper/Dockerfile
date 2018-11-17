FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /2_mapper_bundle

RUN pip3 install zmq

COPY ./2_mapper /2_mapper_bundle/2_mapper
COPY ./mapper /2_mapper_bundle/mapper
COPY ./middleware /2_mapper_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "2_mapper" ]
