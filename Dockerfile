FROM ubuntu:16.10

#2.7
ENV PYTHON_VERSION 2.7

WORKDIR /app

ADD . /app

ENV PYTHONPATH /app/twitterExtraction;/app/;/app/twitterExtraction/GetOldTweets-python-master/;/app/emotion_tensorflow

RUN apt-get -y update
RUN apt-get -y install software-properties-common
RUN add-apt-repository -y ppa:mc3man/trusty-media
RUN apt-get -y install ffmpeg
RUN apt-get -y install libxml2-dev libxslt-dev python-dev lib32z1-dev
RUN apt-get -y install python-pip

RUN pip install --trusted-host pypi.python.org -r requirements.txt

#CMD ["python", "app/twitterExtraction/retrieveTwitterData.py"]
