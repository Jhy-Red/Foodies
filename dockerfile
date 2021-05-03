# syntax=docker/dockerfile:1
FROM python:3.9-slim
LABEL version ="0.0"

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0


RUN pip install --upgrade pip

WORKDIR /opt/app
COPY requirements.txt /opt/app
RUN pip install -r requirements.txt

WORKDIR /foodies
COPY . .

EXPOSE 5000

CMD ["flask", "run"]