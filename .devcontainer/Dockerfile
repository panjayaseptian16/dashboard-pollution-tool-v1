# app/Dockerfile

FROM python:3.11

WORKDIR /usr/src/

RUN apt update && apt install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/panjayaseptian16/dashboard-pollution-tool-v1 .

RUN pip install -r requirements.txt

EXPOSE 8501
