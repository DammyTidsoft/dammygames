FROM python:3.8


ENV PYTHONUNBUFFERED 1

MAINTAINER Mka-ng

RUN mkdir /report-portal

WORKDIR /report-portal

ADD ./requirements.txt /report-portal/requirements.txt

RUN apt-get update

RUN apt-get install python3-dev default-libmysqlclient-dev  -y

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
ADD . /tajnid
EXPOSE 8800
CMD ["python", "manage.py", "runserver", "0.0.0.0:8800"]
