FROM ubuntu:bionic

RUN apt-get -qq update && \
    apt-get -qq install \
    python3-dev \
    python3-pip

COPY ./target/requirements.txt /opt/requirements.txt

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r /opt/requirements.txt

COPY ./target/src /opt/discord-poll-bot

RUN ln -s /opt/discord-poll-bot/pollbot.py /usr/local/bin/
