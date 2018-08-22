#!/usr/bin/env bash

set -ex

VERSION=$1

if [ "" == "$VERSION" ]; then
    echo "Failed to specify version required"
    exit 1
fi

mkdir -p h3/out
rm -rf h3c
git clone https://github.com/uber/h3.git h3c

pushd h3c
git pull origin master --tags
git checkout "$VERSION"

# Run CMake, installing a recent version if not found or not compatible
{
	cmake -DENABLE_FORMAT=OFF -DBUILD_SHARED_LIBS=ON .
} || {
	# Install modern CMake
	mkdir cmake-download
	pushd cmake-download
	curl -O https://cmake.org/files/v3.10/cmake-3.10.0-rc5-Linux-x86_64.sh
	bash cmake-3.10.0-rc5-Linux-x86_64.sh --skip-license
	export PATH=`pwd`/bin:$PATH
	echo $PATH
	popd
	cmake -DENABLE_FORMAT=OFF -DBUILD_SHARED_LIBS=ON .
}

make
ls -l lib/libh3*
cp lib/libh3* ../h3/out
if [ -e ../build ] && [ -d ../build ]; then
    LIBNAME=`ls ../build/ | grep '^lib'`
    mkdir -p ../build/$LIBNAME/h3/out
    cp lib/libh3* ../build/$LIBNAME/h3/out
fi
popd
rm -rf h3c
