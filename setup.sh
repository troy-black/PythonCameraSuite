#!/bin/bash

# Default variables
APP="PythonCameraSuite"
APP_REPOSITORY="https://github.com/troy-black/PythonCameraSuite.git"
HOSTNAME="camerasuite"
UTF_8_LOCAL="en_US.UTF-8"

# System variables
OS="unknown"
VERSION="unknown"
PYTHON="python3"
VENV_ACTIVATION="source venv/bin/activate"

cloneGitRepo() {
    if [[ "${PWD##*/}" == "${APP}" ]]; then
        git pull
    else
        git clone "${APP_REPOSITORY}"
        cd "${APP}"/
    fi
}

createVenv() {
    if [[ "${PWD##*/}" == "${APP}" ]]; then
        if [[ -d "venv" ]]; then
            rm -rf venv
        fi
        "${PYTHON}" -m venv venv
        updateVenv
    fi
}

enableRaspberryPiCamera() {
    sudo raspi-config nonint do_camera 0
}

enableSsh() {
    sudo systemctl enable ssh
    sudo systemctl start ssh
}

getOs() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VERSION=$VERSION_ID
    else
        OS=$(uname -s)
        VERSION=$(uname -r)
        case "${OS}" in
            CYGWIN* | MINGW*)
                OS="Windows"
                PYTHON="python"
                VENV_ACTIVATION="source venv/Scripts/activate"
            ;;
        esac
    fi
}

installUv4l() {
    url="http://www.linux-projects.org/listing/uv4l_repo"
    if ! grep -q "${url}" /etc/apt/sources.list; then
        curl ${url}/lpkey.asc | sudo apt-key add -
        echo "deb ${url}/raspbian/stretch stretch main" | sudo tee -a /etc/apt/sources.list
        sudo apt-get update -y
    fi
    sudo apt-get install -y uv4l uv4l-raspicam uv4l-raspicam-extras uv4l-webrtc uv4l-raspidisp uv4l-raspidisp-extras
}

opencvPrerequisites() {
    sudo apt-get install -y build-essential cmake pkg-config gfortran python3-pyqt5
    sudo apt-get install -y libatlas-base-dev libavcodec-dev libavformat-dev libcairo2-dev libfontconfig1-dev
    sudo apt-get install -y libgdk-pixbuf2.0-dev libgtk-3-dev libgtk2.0-dev libhdf5-103 libhdf5-dev libhdf5-serial-dev
    sudo apt-get install -y libjasper-dev libjpeg-dev libpango1.0-dev libpng-dev libqt4-test libqtgui4 libqtwebkit4
    sudo apt-get install -y libswscale-dev libtiff5-dev libv4l-dev libx264-dev libxvidcore-dev
    sudo apt-get install -y libilmbase-dev libopenexr-dev libgstreamer1.0-dev
}

raspbianPrerequisites() {
    sudo apt-get install -y git vim-nox p7zip-full
}

setHostname() {
    echo "camerasuite" | sudo tee /etc/hostname
}

setLocal() {
    if [[ "${UTF_8_LOCAL} UTF-8" != "$(tail -n 1 /etc/locale.gen)" ]]; then
        echo "${UTF_8_LOCAL} UTF-8" | sudo tee -a /etc/locale.gen
        sudo locale-gen "${UTF_8_LOCAL}"
        sudo update-locale "${UTF_8_LOCAL}"
    fi
}

updateOs() {
    sudo apt-get update -y
    sudo apt-get upgrade -y
}

updateVenv() {
    if [ "${PWD##*/}" == "${APP}" ] && [ -d "venv" ]; then
        ${VENV_ACTIVATION}

        # update pip
        pip install --upgrade --no-cache-dir pip
        pip install --upgrade --no-cache-dir setuptools
        pip install --upgrade --no-cache-dir wheel

        # install/update project in dev mode
        pip install --upgrade --no-cache-dir -v -e .[all]
    fi
}

venvPrerequisites() {
    sudo apt-get install -y python3
    sudo apt-get install -y python3-pip
    sudo apt-get install -y python3-venv
    sudo apt-get install -y python3-dev
}

help() {
    echo "
        usage:
        -----
        setup.sh [ a ] [ u ] [ v ] [ h ]
        description:
        ----------
        Setup bash script for ${APP}
        ---------------
        a | all             Runs all setup tasks.
        u | update          Update everything.
        v | venv            Create new python virtual environment.
        h | help            This helpful bit of info.
        "
}

all() {
    # enable verbose and exit on error
    set -ex

    getOs
    if [[ "${OS}" == "Raspbian GNU/Linux" ]]; then
        updateOs
        raspbianPrerequisites
        enableSsh
        setLocal
        setHostname
        enableRaspberryPiCamera
        installUv4l
        opencvPrerequisites
        venvPrerequisites
    fi
    cloneGitRepo
    createVenv
    if [[ "${OS}" == "Raspbian GNU/Linux" ]]; then
        shutdown -r now
    fi
}

newVenv() {
    # enable verbose and exit on error
    set -ex

    getOs
    if [[ "${OS}" == "Raspbian GNU/Linux" ]]; then
        venvPrerequisites
    fi
    createVenv
}

updateAll() {
    # enable verbose and exit on error
    set -ex

    getOs
    if [[ "${OS}" == "Raspbian GNU/Linux" ]]; then
        updateOs
        venvPrerequisites
        cloneGitRepo
    fi
    updateVenv
}

case "$1" in
    a | all)
        all
        ;;
    u | update)
        updateAll
        ;;
    v | venv)
        createVenv
        ;;
    h | help | *)
        help
        ;;
esac

set +ex
