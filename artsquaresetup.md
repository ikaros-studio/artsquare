# 1. Install PI dependancies

# 2. Install Waveshare Dependancies

# 3. Install ONNX Stream for 


## Install XNNPACK

    check if `$sudo apt-get install cmake` is installed

    - Build XNNPACK
    $cd ~/XNNPACK
    mkdir build
cd build

cmake -DXNNPACK_BUILD_TESTS=OFF -DXNNPACK_BUILD_BENCHMARKS=OFF ..

cmake --build . --config Release

## Install OnnxStream

cd ~
git clone https://github.com/vitoplantamura/OnnxStream.git
cd OnnxStream/src
mkdir build
cd build
cmake -DMAX_SPEED=ON -DOS_LLM=OFF -DOS_CUDA=OFF -DXNNPACK_DIR=~/XNNPACK ..
cmake --build . --config Release


## Run 



