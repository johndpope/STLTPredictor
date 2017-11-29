FROM python:2.7

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

#CMD ["python", "app/twitterExtraction/retrieveTwitterData.py"]
