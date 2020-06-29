import re
import os
import argparse
import string
import shutil
import tempfile

LINARO_GNU_TOOLCHAIN_ARCHITECTURES = {
    'arm32-v7': 'arm-linux-gnueabihf',
    'arm32-v8': 'armv8l-linux-gnueabihf',
    'arm64-v8': 'aarch64-linux-gnu'
}

LINARO_GNU_TOOLCHAIN_VERSIONS = [
    '6.3.1-2017.05',
    '6.4.1-2018.05',
    '6.5.0-2018.12',
    '7.1.1-2017.08',
    '7.2.1-2017.11',
    '7.3.1-2018.05',
    '7.4.1-2019.02',
    '7.5.0-2019.12',
]

LINARO_GNU_TOOLCHAIN_NAME = string.Template('gcc-linaro-$version-x86_64_$arch')
LINARO_GNU_TOOLCHAIN_URL = string.Template('https://releases.linaro.org/components/toolchain/binaries/$version/$arch/$name.tar.xz')

WGET_COMMAND = string.Template('wget --quiet $url -O $output')
TAR_COMMAND = string.Template('tar -xf $archive -C $output --strip-components=1')

PATCH_VERSION_REGEX = re.compile(r'.[0-9]-')

def check_tool_available(name):
    assert shutil.which(name) is not None, "Tool `{}` is not avaialble in your system PATH.".format(name)

def main():
    parser = argparse.ArgumentParser(description='Download and install Linaro GNU Toolchain.')
    parser.add_argument('-a', '--architecture', choices=['arm32-v7', 'arm32-v8', 'arm64-v8'], required=True, help='Toolchain architecture for Arm.')
    parser.add_argument('-v', '--version', choices=LINARO_GNU_TOOLCHAIN_VERSIONS, required=True, help='Toolchain version to download.')
    parser.add_argument('-o', '--output', default='/usr/local/linaro-gnu-toolchain', help='Location where to save toolchain.')
    args = parser.parse_args()

    arch = LINARO_GNU_TOOLCHAIN_ARCHITECTURES[args.architecture]

    toolchain = LINARO_GNU_TOOLCHAIN_NAME.substitute(
        version=args.version,
        arch=arch
    )

    url = LINARO_GNU_TOOLCHAIN_URL.substitute(
        version=PATCH_VERSION_REGEX.sub('-', args.version),
        arch=arch,
        name=toolchain)

    check_tool_available('wget')
    check_tool_available('tar')

    tmp_file = '/tmp/linaro-gnu-toolchain.tar.xz'
    
    wget_cmd = WGET_COMMAND.substitute(
        url=url,
        output=tmp_file)

    print(wget_cmd)

    os.system(wget_cmd)

    tar_cmd = TAR_COMMAND.substitute(
        archive=tmp_file,
        output=args.output)

    print(tar_cmd)

    os.makedirs(args.output, exist_ok=True)
    os.system(tar_cmd)

    os.remove(tmp_file)

if __name__ == '__main__':
    main()
