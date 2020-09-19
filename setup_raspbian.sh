#!/bin/bash

# enable verbose and exit on error
set -ex

# update / upgrade
sudo apt-get update -y && sudo apt-get upgrade -y

# enable ssh
sudo systemctl enable ssh
sudo systemctl start ssh

# change local to US English
echo 'en_US.UTF-8 UTF-8' | sudo tee -a /etc/locale.gen
echo 'LANG=en_US.UTF-8' | sudo tee -a /etc/default/locale
sudo locale-gen en_US.UTF-8
sudo update-locale en_US.UTF-8

# change hostname
echo 'camerasuite' | sudo tee /etc/hostname

# enable pi camera module
sudo raspi-config nonint do_camera 0

# prerequisites for opencv
sudo apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5 -y

# install uv4l
curl http://www.linux-projects.org/listing/uv4l_repo/lpkey.asc | sudo apt-key add -
echo 'deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/stretch stretch main' | sudo tee -a /etc/apt/sources.list
sudo apt-get update -y
sudo apt-get install -y uv4l uv4l-raspicam uv4l-raspicam-extras uv4l-webrtc uv4l-raspidisp uv4l-raspidisp-extras

# install git and vim
sudo apt-get install git vim-nox -y

# clone git repo
git clone https://github.com/troy-black/PythonCameraSuite.git
cd PythonCameraSuite

# install python3 dependencies
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y
sudo apt-get install python3-venv -y
sudo apt-get install python3-dev -y

# create venv
bash create_venv.sh
