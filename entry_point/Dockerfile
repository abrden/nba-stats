FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /ep

RUN pip3 install zmq

COPY ./entry_point /ep/entry_point
COPY ./NBA-shot-log  /ep/NBA-shot-log
COPY ./NBA-shot-log-sample  /ep/NBA-shot-log-sample
COPY ./middleware /ep/middleware

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "entry_point" ]
