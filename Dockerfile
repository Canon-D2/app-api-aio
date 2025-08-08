# Base image
FROM python:3.12-alpine

# Set working directory
WORKDIR /opt/python-projects/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
    libressl-dev libffi-dev gcc musl-dev python3-dev \
    && pip install --upgrade pip setuptools wheel \
    && apk add curl openssl \
    && rm -rf /root/.cache/pip

# Copy requirements and install
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project source code
COPY . .

# Optional: expose FastAPI port
EXPOSE 8000
