FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    unzip \
    cmake \
    wget \
    git \
    vim \
    nano \
    python3-dev \
    python3-pip \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

