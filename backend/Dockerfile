FROM python:3.10.6

WORKDIR /code

COPY ./ /code/app

RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt

EXPOSE 8080

WORKDIR /code
