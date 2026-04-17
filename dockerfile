FROM python:3.11-slim

ARG TERRAFORM_VERSION=1.14.8

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt .

RUN set -eux; \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        wget unzip git ca-certificates uuid-runtime && \
    \
    # Terraform
    wget -q https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    unzip -q terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/local/bin && \
    rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    \
    # Python reqs
    pip install --no-cache-dir -r requirements.txt && \
    \
    # Clean up
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
