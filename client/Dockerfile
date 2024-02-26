FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/client/

ENV PYTHONPATH "${PYTHONPATH}:/code/client/"

CMD ["pytest"]
