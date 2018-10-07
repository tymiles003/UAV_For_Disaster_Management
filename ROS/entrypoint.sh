#!/bin/bash

useradd --shell /bin/bash -c "" -m $USERNAME

export HOME=/home/$USERNAME
export PATH=/home/$USERNAME/bin:/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin:/home/$USERNAME/.local/bin/:/usr/local

usermod -aG sudo $USERNAME
echo "$USERNAME:test" | chpasswd

exec /usr/local/bin/gosu $USERNAME "$@"