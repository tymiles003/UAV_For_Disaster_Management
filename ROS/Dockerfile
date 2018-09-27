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
    sudo \
    build-essential \
    python3-dev \
    python3-pip \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

RUN echo "deb http://packages.ros.org/ros/ubuntu xenial main" > /etc/apt/sources.list.d/ros-latest.list && \
    apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116 && \
    apt-get update

RUN pip3 install --upgrade pip

COPY requirements.txt /home
RUN cd /home && \
    pip3 install -r requirements.txt 

RUN apt-get install -y \
    libboost-all-dev \
    libboost-python-dev \
    libeigen3-dev \
    libyaml-cpp-dev \
    python3-sip \
    python3-sip-dev \
    python3-setuptools 

RUN cd /usr/bin && ln -sf python3 python

RUN cd /usr/lib/x86_64-linux-gnu && ln -s libboost_python-py35.so libboost_python3.so

RUN rosdep init \
    && rosdep update

RUN mkdir /root/ros_catkin_ws

RUN cd /root/ros_catkin_ws && rosinstall_generator desktop_full --rosdistro kinetic --deps --wet-only --tar > kinetic-desktop-full-wet.rosinstall
RUN cd /root/ros_catkin_ws && wstool init -j8 src kinetic-desktop-full-wet.rosinstall

RUN cd /root/ros_catkin_ws && ./src/catkin/bin/catkin_make_isolated -DPYTHON_VERSION=3.5 \
    --install -DCMAKE_BUILD_TYPE=Release
