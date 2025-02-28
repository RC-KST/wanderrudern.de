#!/usr/bin/bash
WDIR=$(realpath $(dirname $0))
echo WORKING_DIR: $WDIR

PUBLIC_PATH=$(realpath "$WDIR/../public")

UTIL_HASHING_PATH=$(realpath --canonicalize-missing "$WDIR/../util_hashing")
HASHES_FILE="$UTIL_HASHING_PATH/hashes.chk"

mkdir -p $UTIL_HASHING_PATH

# Clean hashes file
printf "" > $HASHES_FILE
find $PUBLIC_PATH -type f | xargs -L100 sha256sum >> $HASHES_FILE
