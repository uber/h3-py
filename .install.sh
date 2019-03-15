#!/usr/bin/env bash

set -ex

VERSION=$1

if [ "" == "$VERSION" ]; then
    echo "Failed to specify version required"
    exit 1
fi

command -v cmake  >/dev/null 2>&1 || { echo "cmake required but not found."; exit 1; }

mkdir -p h3/out
rm -rf h3c
git clone https://github.com/uber/h3.git h3c

pushd h3c
git pull origin master --tags
git checkout "$VERSION"

if command -v make; then
  command -v cc  >/dev/null 2>&1 || { echo "cc required but not found."; exit 1; }

  cmake -DENABLE_FORMAT=OFF -DBUILD_SHARED_LIBS=ON .

  make
  ls -l lib/libh3*
  cp lib/libh3* ../h3/out
  if [ -e ../build ] && [ -d ../build ]; then
      LIBNAME=`ls ../build/ | grep '^lib'`
      mkdir -p ../build/$LIBNAME/h3/out
      cp lib/libh3* ../build/$LIBNAME/h3/out
  fi
else
  # Assumed to be Windows, default to x64
  if [[ "$PYTHON_ARCH" == "32" ]]; then
    cmake . -DENABLE_FORMAT=OFF -DBUILD_SHARED_LIBS=ON -DCMAKE_VS_PLATFORM_NAME=$PLATFORM
  else
    cmake . -DENABLE_FORMAT=OFF -DBUILD_SHARED_LIBS=ON -DCMAKE_VS_PLATFORM_NAME=$PLATFORM -G "Visual Studio 14 Win64"
  fi
  cmake --build . --target h3 --config Release
  ls -l bin/Release/*
  cp bin/Release/h3.dll ../h3/out
fi
popd
rm -rf h3c
