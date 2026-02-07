FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    cmake \
    gcc \
    g++ \
    clang-format \
    libboost-dev \
    libboost-program-options-dev \
    openmpi-bin \
    openmpi-doc \
    libopenmpi-dev \
    python3 \
    python3-pip \
    python3-venv \
    wget \
    curl \
    autoconf \
    automake \
    libtool \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Build and install protobuf from source (required by ASTRA-sim)
RUN git clone --depth 1 --branch v3.21.12 https://github.com/protocolbuffers/protobuf.git /tmp/protobuf && \
    cd /tmp/protobuf && \
    git submodule update --init --recursive && \
    mkdir build && cd build && \
    cmake ../cmake -DCMAKE_INSTALL_PREFIX=/usr/local \
        -Dprotobuf_BUILD_TESTS=OFF \
        -DCMAKE_POSITION_INDEPENDENT_CODE=ON && \
    make -j$(nproc) && make install && ldconfig && \
    rm -rf /tmp/protobuf

# Clone ASTRA-sim with submodules
RUN git clone --recurse-submodules https://github.com/astra-sim/astra-sim.git

WORKDIR /app/astra-sim

# Build the analytical backend
RUN ./build/astra_analytical/build.sh

# Install Python packages for Chakra trace conversion
RUN pip3 install protobuf pydot

# Install Chakra from the bundled submodule
RUN cd /app/astra-sim/extern/graph_frontend/chakra && \
    pip3 install . 2>/dev/null || \
    pip3 install -e . 2>/dev/null || true

# Get the ResNet-50 workload from v1.0 branch
RUN git fetch origin ASTRA-sim-1.0 && \
    git show origin/ASTRA-sim-1.0:inputs/workload/Resnet50_DataParallel.txt > /app/Resnet50_DataParallel.txt || true

# Copy the run script
COPY run_resnet50.sh /app/run_resnet50.sh
RUN chmod +x /app/run_resnet50.sh

WORKDIR /app
