#!/bin/bash
set -e -x

for PYBIN in /opt/python/cp3{6,7}-*/bin; do
    "${PYBIN}/pip" install -r /io/requirements-dev.txt
    ln -f -s "${PYBIN}/cmake" /usr/bin/cmake
    echo `which cmake`
    "${PYBIN}/pip" wheel /io/ -w wheelhouse/
done

for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" -w /io/wheelhouse/
done

for PYBIN in /opt/python/cp3{6,7}-*/bin; do
	"${PYBIN}/pip" install h3cy --no-index --find-links /io/wheelhouse
    "${PYBIN}/pytest" --verbose --tb=line -s /io/test/
done

