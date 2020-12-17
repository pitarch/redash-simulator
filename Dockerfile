FROM python:3.7-alpine

COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY entrypoint.sh /
COPY app/ /app
WORKDIR /

CMD ["/entrypoint.sh"]
