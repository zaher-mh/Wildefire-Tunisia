FROM python:2.7.13-slim
MAINTAINER Zaher

RUN  apt-get update && apt-get install -y build-essential libssl-dev libffi-dev python-dev

WORKDIR /
ADD requirements.txt /
RUN pip install -r requirements.txt

ADD . /

EXPOSE 8080

CMD ["python","web_app.py"]