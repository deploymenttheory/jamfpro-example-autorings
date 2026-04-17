FROM python:3.11-slim

ARG TERRAFORM_VERSION=1.14.8
ARG GH_VERSION=2.62.0

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt .
COPY ./go-jamf-guid-sharder /usr/local/bin/sharder
RUN chmod +x /usr/local/bin/sharder

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
    # gh CLI
    wget -q https://github.com/cli/cli/releases/download/v${GH_VERSION}/gh_${GH_VERSION}_linux_amd64.tar.gz && \
    tar -xzf gh_${GH_VERSION}_linux_amd64.tar.gz && \
    mv gh_${GH_VERSION}_linux_amd64/bin/gh /usr/local/bin/ && \
    rm -rf gh_${GH_VERSION}_linux_amd64* && \
    \
    # Python reqs
    pip install --no-cache-dir -r requirements.txt && \
    \
    # Clean up
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
