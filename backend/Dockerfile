FROM python:3.9-alpine
ADD settings settings
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apk add --no-cache libffi-dev
RUN apk add build-base
RUN apk add --no-cache supervisor \
    && python -m pip install --upgrade pip \
    && pip install -r requirements.txt
COPY ./ /code/
RUN pip install -e .
CMD ["pruefstelle", "run"]



