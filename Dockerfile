FROM python:3
ENV PYTHONUNBUFFERED 1
ENV CURR_LAYER_ACCESS_KEY c777d6e7d573fe0a7708d564cca8c836
ENV DATABASE_URL postgres://postgres:postgres@db/postgres
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/