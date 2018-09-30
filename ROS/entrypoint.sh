#!/bin/bash

useradd --shell /bin/bash -c "" -m $USERNAME

export HOME=/bome/$USERNAME
export PATH=/home/$USERNAME/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/$USERNAME/.local/bin/:/usr/local

usermod -aG sudo $USERNAME
echo "$USERNAME:test" | chpasswd

source /root/ros_catkin_ws/install_isolated/setup.bash
