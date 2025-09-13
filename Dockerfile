# Base image
FROM python:3.12-alpine

# Set work directory
WORKDIR /opt/python-projects/app

# Env settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-adeps build-base \
    openssl-dev libffi-dev gcc musl-dev python3-dev librdkafka-dev \
    && pip install --upgrade pip setuptools wheel \
    && rm -rf /root/.cache/pip

# Copy requirements file
COPY ./requirements.txt /opt/python-projects/app/requirements.txt

# Install Python dependencies
RUN pip install -r /opt/python-projects/app/requirements.txt

# Install extra tools for healthcheck and SSL
RUN apk add --no-cache curl openssl

# Copy project files
COPY . /opt/python-projects/app/
