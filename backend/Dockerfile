FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./ /code/
RUN pip install -e .
ENV ENV_FOR_PRUEFSTELLE=production
EXPOSE 8000
CMD ["pruefstelle", "run", "--proxy-headers", "--with-populate"]



