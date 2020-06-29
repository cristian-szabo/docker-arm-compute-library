import re
import os
import argparse
import shutil
import tempfile
import string
import multiprocessing

ARM_COMPUTE_LIBRARY_ARCHITECTURES = {
    'arm32-v7': 'armv7a',
    'arm32-v8': 'armv8a',
    'arm64-v8': 'arm64-v8a'
}

ARM_COMPUTE_LIBRARY_VERSIONS = [
    '20.05',
    '20.02.1',
    '19.11.1',
    '19.08.1',
    '19.05',
    '19.02',
]

ARM_COMPUTE_LIBRARY_URL = 'https://github.com/ARM-software/ComputeLibrary.git'

GIT_CLONE_COMMAND = string.Template('git clone --quiet --depth 1 --branch v$version $url $path')
SCONS_BUILD_COMMAND = string.Template('scons --silent -C $source_dir install_dir=$install_dir os=linux arch=$arch neon=1 opencl=0 embed_kernels=0 gemm_tuner=0 examples=0 benchmark_examples=0 validate_examples=0 reference_openmp=0 -j$cores')

def check_tool_available(name):
    assert shutil.which(name) is not None, "Tool `{}` is not avaialble in your system PATH.".format(name)

def main():
    parser = argparse.ArgumentParser(description='Build and install Arm Compute Library.')
    parser.add_argument('-a', '--architecture', choices=['arm32-v7', 'arm32-v8', 'arm64-v8'], required=True, help='Build architecture for Arm.')
    parser.add_argument('-v', '--version', choices=ARM_COMPUTE_LIBRARY_VERSIONS, required=True, help='Library version to download.')
    parser.add_argument('-s', '--operating-system', choices=['linux', 'android'], required=True, help='Operating system to target build libraries.')
    parser.add_argument('-o', '--output', default='/usr/local/arm-compute-library', help='Location where to install libraries.')
    args = parser.parse_args()

    check_tool_available('git')
    check_tool_available('scons')

    tmp_dir = '/tmp/acl'
    
    git_clone_cmd = GIT_CLONE_COMMAND.substitute(
        url=ARM_COMPUTE_LIBRARY_URL,
        version=args.version,
        path=tmp_dir)

    print(git_clone_cmd)

    os.system(git_clone_cmd)

    scons_build_cmd = SCONS_BUILD_COMMAND.substitute(
        source_dir=tmp_dir,
        install_dir=args.output,
        arch=ARM_COMPUTE_LIBRARY_ARCHITECTURES[args.architecture],
        os=args.operating_system,
        cores=multiprocessing.cpu_count())

    print(scons_build_cmd)

    os.system(scons_build_cmd)

    shutil.rmtree(tmp_dir)

if __name__ == '__main__':
    main()
