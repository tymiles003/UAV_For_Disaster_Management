FROM ubuntu:16.04

RUN apt-get update && apt-get install -y apt-utils apt-transport-https \
    curl \
    gcc \
    g++ \
    unzip \
    cmake \
    wget \
    git \
    vim \
    sudo \
    tar \
    software-properties-common \
    pkg-config \
    build-essential \
    python3-dev \
    python3-pip \
    python3-setuptools \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

RUN echo "deb http://packages.ros.org/ros/ubuntu xenial main" > /etc/apt/sources.list.d/ros-latest.list && \
    apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116 && \
    apt-get update

RUN apt-get update && apt-get install -y \
    xorg-dev \
    libgl1-mesa-dev \
    xvfb \
    libxinerama1 \
    libxcursor1 \
    unzip \
    libglu1-mesa \
    libav-tools \
    libpq-dev \
    libjpeg-dev \
    libboost-all-dev \
    && apt-get clean \
    && apt-get autoremove

RUN pip3 install \
    numpy \
    matplotlib \
    rosdep \
    rosinstall_generator \
    rospkg \
    rosinstall \
    catkin_pkg \
    catkin_tools \
    empy \
    trollius \
    wstool \
    pyqt5 \
    && pip3 uninstall vcstools \ 
    && pip3 install git+https://github.com/tkruse/vcstools.git@mock_server_tar_test

RUN rosdep init \
    && rosdep update

RUN mkdir /root/ros_catkin_ws \
    && cd /root/ros_catkin_ws \
    && rosinstall_generator desktop_full --rosdistro kinetic --deps --wet-only --tar > kinetic-desktop-full-wet.rosinstall \
    && wstool init -j8 src kinetic-desktop-full-wet.rosinstall

RUN cd /usr/bin \
    && ln -sf python3 python

RUN apt-get update && apt-get install -y \
    libconsole-bridge-dev \
    libtinyxml-dev \
    liblz4-dev \
    libbz2-dev \
    liburdfdom-dev \
    libpoco-dev \
    libtinyxml2-dev \
    libeigen3-dev \
    python3-sip \
    python3-sip-dev \
    libyaml-cpp-dev \
    libboost-python-dev \
    qt5-default \
    libfltk1.3-dev \
    libcurl4-gnutls-dev \
    assimp \
    assimp-utils \
    uuid-dev \
    uuid-runtime 

RUN cd /usr/lib/x86_64-linux-gnu/ \
    && ln -s libboost_python-py35.so libboost_python3.so

RUN cd /root/ros_catkin_ws \
    && catkin config --init \
    && catkin build --cmake-args -DPYTHON_VERSION=3.5 -DCMAKE_BUILD_TYPE=Release -DCATKIN_ENABLE_TESTING=OFF

RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 && \
    curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/1.10/gosu-$(dpkg --print-architecture)" \
        && curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/1.10/gosu-$(dpkg --print-architecture).asc" \
            && gpg --verify /usr/local/bin/gosu.asc \
                && rm /usr/local/bin/gosu.asc \
                    && chmod +x /usr/local/bin/gosu

RUN ldconfig

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
ENTRYPOINT ["sh","/usr/local/bin/entrypoint.sh"]