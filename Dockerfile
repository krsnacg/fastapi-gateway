FROM python:3.13.5-slim-bookworm

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./configuration /code/configuration

CMD [ "fastapi", "run", "app/main.py", "--port", "8090"]