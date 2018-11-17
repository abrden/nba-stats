FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /32_mapper_bundle

RUN pip3 install zmq

COPY ./32_mapper /32_mapper_bundle/32_mapper
COPY ./mapper /32_mapper_bundle/mapper
COPY ./middleware /32_mapper_bundle/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "32_mapper" ]
