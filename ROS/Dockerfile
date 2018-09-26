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
    build-essential \
    python3-dev \
    python3-pip \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

RUN echo "deb http://packages.ros.org/ros/ubuntu xenial main" > /etc/apt/sources.list.d/ros-latest.list && \
    apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116 && \
    apt-get update

RUN apt-get install -y \
    libeigen3-dev \
    python3-sip \
    python3-sip-dev \
    python3-setuptools 