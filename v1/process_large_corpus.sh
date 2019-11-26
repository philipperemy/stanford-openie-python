#!/usr/bin/env bash

set -e

if [[ $# -eq 0 ]] ; then
    echo 'Please give two arguments to the script: [input_filename] [output_filename].'
    exit 0
fi

# On Mac OS - brew install coreutils
# On linux: split

TMP_DIR=/tmp/openie/large_corpus

rm -rf $TMP_DIR
mkdir -p $TMP_DIR

if [ "$(uname)" == "Darwin" ]; then
    gsplit -b 10k --numeric-suffixes $1 ${TMP_DIR}/small_
else
    split -b 10k --numeric-suffixes $1 ${TMP_DIR}/small_
fi

num_files=$(find ${TMP_DIR}/small_* -type f | wc -l)
var=1
for file in ${TMP_DIR}/small_*
do
    if [[ -f $file ]]; then
        echo "(${var} / ${num_files}) python main.py -f $file > $file.out"
        python main.py -f $file > $file.out
        var=$((var + 1))
    fi
done

cat ${TMP_DIR}/*.out > $2
echo "Redirected the output to $2"
