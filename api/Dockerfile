FROM python:3.8

WORKDIR /app/api
COPY requirements.txt /app/api

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /app/api

EXPOSE 80
ENTRYPOINT bash /app/api/entrypoint.sh