FROM python:3
RUN apt-get update && apt-get install -y \
    python3-pip
RUN pip3 install tweepy
RUN pip3 install schedule
RUN pip3 install datetime
WORKDIR /files
