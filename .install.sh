#!/usr/bin/env bash

set -ex

VERSION=$1

if [ "" == "$VERSION" ]; then
    echo "Failed to specify version required"
    exit 1
fi

command -v cmake  >/dev/null 2>&1 || { echo "cmake required but not found."; exit 1; }
command -v make  >/dev/null 2>&1 || { echo "make required but not found."; exit 1; }
command -v cc  >/dev/null 2>&1 || { echo "cc required but not found."; exit 1; }

mkdir -p h3/out
rm -rf h3c
git clone https://github.com/uber/h3.git h3c

pushd h3c
git pull origin master --tags
git checkout "$VERSION"

cmake -DENABLE_FORMAT=OFF -DBUILD_SHARED_LIBS=ON .
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
