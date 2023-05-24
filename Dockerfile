FROM python:3.8-slim-bullseye

COPY utils /app/utils
COPY main.py /app
COPY requirements.txt /app

RUN apt update
RUN apt upgrade
RUN apt install libreoffice -y

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 2000

CMD python main.py --port=2000 --save_dir=saved