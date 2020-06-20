#!/bin/bash
set -e

apt-get update && apt-get install -y --no-install-recommends build-essential \
    nginx \
    libpq-dev \
    python3 \
    python3-dev \
    python3-setuptools \
    python3-pip

# install python requirements
/usr/bin/pip3 install --upgrade pip
pip3 install --no-cache-dir -r /build/requirements.txt
