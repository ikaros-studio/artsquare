# E-Ink Frame Image Generator Documentation

## Overview
This documentation provides a detailed guide on setting up and running an autonomous image frame that utilizes a lightweight generative image model running on a Raspberry Pi 4. The frame uses E-Ink technology to generate and display daily images based on prompts.

## Table of Contents
1. [Installation](#installation)
   - [Install Raspberry Pi Dependencies](#install-raspberry-pi-dependencies)
   - [Install Waveshare Dependencies](#install-waveshare-dependencies)
   - [Install ONNX Stream](#install-onnx-stream)
     - [Install XNNPACK](#install-xnnpack)
     - [Install OnnxStream](#install-onnxstream)
2. [Running the Application](#running-the-application)
3. [Setting Up Cron Job](#setting-up-cron-job)
4. [Handling Power Interruptions](#handling-power-interruptions)
5. [Code Explanation](#code-explanation)
6. [Configuration File](#configuration-file)

## Installation

### Install Raspberry Pi Dependencies
Ensure your Raspberry Pi is up to date and install necessary dependencies:
```sh
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip python3-dev
```
### Install Waveshare Dependencies
Install the required dependencies for the Waveshare E-Ink display:
```sh
pip3 install Pillow
pip3 install spidev
pip3 install RPi.GPIO
pip3 install numpy
```

### Install ONNX Stream

#### Install XNNPACK

1. Check if cmake is installed:

```sh
sudo apt-get install cmake
```
2. Build XNNPACK:

```sh
cd ~
git clone https://github.com/google/XNNPACK.git
cd XNNPACK
mkdir build
cd build
cmake -DXNNPACK_BUILD_TESTS=OFF -DXNNPACK_BUILD_BENCHMARKS=OFF ..
cmake --build . --config Release
```

#### Install OnnxStream
1. Clone the OnnxStream repository

```sh
cd ~
git clone https://github.com/vitoplantamura/OnnxStream.git
cd OnnxStream/src
mkdir build
cd build
```
2. Configure the build with XNNPACK:
```sh
cmake -DMAX_SPEED=ON -DOS_LLM=OFF -DOS_CUDA=OFF -DXNNPACK_DIR=~/XNNPACK ..
```

3. Build OnnxStream:
```sh
cmake --build . --config Release
```

## Runing the Applications and setting the schedulers

To run the script every hour, add a cron job:
```sh
crontab -e
```

Add the following line to the file to run the script at boot:
```sh
@reboot /usr/bin/python3 /home/pi/artsquare/python/prod/generate_image.py
```

## Handling Power Interruptions
Create a startup service to run the script immediately upon boot. Look up the systemd service file in `services/eink_frame.service` and save this file as /etc/systemd/system/eink-image-generator.service and enable it:

```sh
sudo systemctl enable eink-image-generator.service
sudo systemctl start eink-image-generator.service
```


