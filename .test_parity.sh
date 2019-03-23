#!/usr/bin/env bash

VERSION=$1

if [ "" == "$VERSION" ]; then
    echo "Failed to specify version required"
    exit 1
fi

rm -rf h3c
git clone https://github.com/uber/h3.git h3c
pushd h3c
git pull origin master --tags
git checkout "$VERSION"
