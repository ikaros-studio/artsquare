# 1. Install PI dependancies
# 2. Install Waveshare Dependencies

# 3. Install ONNX Stream

## Install XNNPACK

To install XNNPACK, follow these steps:

1. Check if `cmake` is installed by running the command `$sudo apt-get install cmake`.

2. Build XNNPACK:
    ```
    $cd ~/XNNPACK
    mkdir build
    cd build
    cmake -DXNNPACK_BUILD_TESTS=OFF -DXNNPACK_BUILD_BENCHMARKS=OFF ..
    cmake --build . --config Release
    ```

## Install OnnxStream

To install OnnxStream, follow these steps:

1. Clone the OnnxStream repository:
    ```
    cd ~
    git clone https://github.com/vitoplantamura/OnnxStream.git
    cd OnnxStream/src
    mkdir build
    cd build
    ```

2. Configure the build with XNNPACK:
    ```
    cmake -DMAX_SPEED=ON -DOS_LLM=OFF -DOS_CUDA=OFF -DXNNPACK_DIR=~/XNNPACK ..
    ```

3. Build OnnxStream:
    ```
    cmake --build . --config Release
    ```

## Run

To run the application, follow the instructions provided in the documentation.



## add cron Job

0 * * * * /usr/bin/python3 /path/to/your/script.py


## Handling Power Interruptions:
Create a startup service to run the script immediately upon boot. Create a systemd service file:

[Unit]
Description=E-Ink Frame Image Generator
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/your/script.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
Save this file as /etc/systemd/system/eink-image-generator.service and enable it:


Save this file as /etc/systemd/system/eink-image-generator.service and enable it:

sh
Copy code
sudo systemctl enable eink-image-generator.service
sudo systemctl start eink-image-generator.service