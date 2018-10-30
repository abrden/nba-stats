FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /ep

RUN pip3 install zmq

COPY ./entry_point /ep/entry_point

ENTRYPOINT [ "python3" ]

CMD [ "-u", "-m", "entry_point" ]
