#!/usr/bin/bash
REMOTE_WDIR=""
WDIR=$(realpath $(dirname $0))
echo WORKING_DIR: $WDIR

# INFO: hashes.chk has to exist, it is used for diffing files
UTIL_HASHING_PATH=$(realpath --canonicalize-missing "$WDIR/../util_hashing")
SFTP_BATCH_FILE="$UTIL_HASHING_PATH/update.sftp"
HASHES_FILE="$UTIL_HASHING_PATH/hashes.chk"
PUBLIC_PATH=$(realpath "$WDIR/../public")

mkdir -p $UTIL_HASHING_PATH;
test -e "$HASHES_FILE" || touch $HASHES_FILE

CHANGED=($(sha256sum --ignore-missing -c $HASHES_FILE | awk 'match($0, /^([^:]*): +FAILED/, a) { print a[1] }'))

REMOVED=($(diff <(cat $HASHES_FILE | cut -f3 -d ' ' | sort) \
    <(find $PUBLIC_PATH -type f | xargs realpath | sort) \
    | grep '^<' | cut -d ' ' -f2))

ADDED=($(diff <(cat $HASHES_FILE | cut -f3 -d ' ' | sort) \
    <(find $PUBLIC_PATH -type f | xargs realpath | sort) \
    | grep '^>' | cut -d ' ' -f2))

PUT_FILES=("${ADDED[@]}" "${CHANGED[@]}")
RM_FILES=("${REMOVED[@]}")

echo changed:
for file in "${CHANGED[@]}"; do
    printf "\t%s\n" $file
done
echo removed:
for file in "${REMOVED[@]}"; do
    printf "\t%s\n" $file
done
echo added:
for file in "${ADDED[@]}"; do
    printf "\t%s\n" $file
done

printf "\n\n"

#echo put:
#for file in "${PUT_FILES[@]}"; do
#    printf "\t%s\n" $file
#done
#echo rm:
#for file in "${RM_FILES[@]}"; do
#    printf "\t%s\n" $file
#done

# Clear and rewrite header section sftp script
mkdir -p 
cat >$SFTP_BATCH_FILE << EOF

EOF

echo "put:"
for file in "${PUT_FILES[@]}"; do
    file_remote=$REMOTE_WDIR/$(realpath --relative-to $PUBLIC_PATH $file)
    dir=$(dirname $file_remote)
    echo "  $file -> $file_remote" 

    cat >>$SFTP_BATCH_FILE << EOF
mkdir -p -f "$dir";
put "$file" -o "$file_remote";
EOF
done

printf "\n" >> $SFTP_BATCH_FILE

echo "rm:"
for file in "${RM_FILES[@]}"; do
    file_remote=$REMOTE_WDIR/$(realpath --canonicalize-missing --relative-to $PUBLIC_PATH $file)
    echo "  $file -> $file_remote" 
    cat >>$SFTP_BATCH_FILE << EOF
rm -r -f "$file_remote";
EOF
done

cat >>$SFTP_BATCH_FILE << EOF
bye;

EOF

echo ================== OUTPUT FILE ==================

cat $SFTP_BATCH_FILE
