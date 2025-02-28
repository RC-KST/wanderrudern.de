#!/usr/bin/bash
WDIR=$(realpath $(dirname $0))
echo WORKING_DIR: $WDIR

PROJECT_DIR=$(realpath $WDIR/..)

cd $PROJECT_DIR

echo hugo build in: $PWD
hugo build --cleanDestinationDir --baseURL https://couchramen-it.de --minify
