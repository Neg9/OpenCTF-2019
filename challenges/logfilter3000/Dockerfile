FROM python:3.7

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install -r /code/requirements.txt 

COPY ./simple_orm /code/simple_orm
COPY ./setup.py /code
RUN pip3 install .

COPY ./web /code/web
WORKDIR /code/web

CMD ["python3", "./app.py"]

EXPOSE 5000
