#!/bin/bash
mkdir -p taco
mkdir=`pwd`/taco/tmp
MYDIR=`pwd`/taco
cd taco-oopsla2017
cmake -DCMAKE_BUILD_TYPE=release -DCMAKE_INSTALL_PREFIX=$MYDIR .
make -j
make install
