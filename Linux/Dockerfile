FROM ubuntu:20.04

ARG ARM_COMPUTE_LIBRARY_VERSION=20.05
ARG LINARO_GNU_TOOLCHAIN_VERSION=6.3.1-2017.05
ARG ARM_ARCHITECTURE=arm64-v8

ENV ARM_COMPUTE_LIBRARY_ROOT="/usr/local/arm-compute-library" \
    LINARO_GNU_TOOLCHAIN_ROOT="/usr/local/linaro-gnu-toolchain"
    
ENV DEBIAN_FRONTEND=noninteractive \
    PATH="$LINARO_GNU_TOOLCHAIN_ROOT/bin:$PATH" \
    LD_LIBRARY_PATH="$ARM_COMPUTE_LIBRARY_ROOT/lib:$LD_LIBRARY_PATH"

COPY Scripts/ /scripts

RUN set -x \
    && apt-get update \
    && apt-get install -y git wget scons \
    && python3 /scripts/linaro_gnu_toolchain.py -a $ARM_ARCHITECTURE -v $LINARO_GNU_TOOLCHAIN_VERSION -o $LINARO_GNU_TOOLCHAIN_ROOT \
    && python3 /scripts/arm_compute_library.py -a $ARM_ARCHITECTURE -v $ARM_COMPUTE_LIBRARY_VERSION -s linux -o $ARM_COMPUTE_LIBRARY_ROOT \
    && apt-get autoremove -y scons wget git \
    && apt-get clean \
    && rm -rf /scripts
