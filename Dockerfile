FROM python:3.8.3-buster

RUN mkdir /code/
COPY *.py /code/
COPY requirements.txt /code/

RUN pip3 install -r /code/requirements.txt

ENTRYPOINT [ "python3", "/code/server.py" ]