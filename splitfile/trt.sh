#!/usr/bin/env bash

### Functions

# normal treatment for 500 000  
treatment () {
    # explanation for sort
    #   field 0: Id (numeric)
    #   field 1: Key1 (numeric)
    #   field 2: Key2 (numeric)
    #   field 3: Key3 (numeric)
    #   field 4: Amount (numeric)
    #   separator: blank
    ./generate.py --num $1 | LC_ALL=C sort +1n -2 +2n -3 +3n -4 +4n -5 | ./splitfile.py --gem "gem" --file -
}

# usage
usage () {
    echo "usage : ./trt.sh [[-h] | [--help]]  print this"
    echo "     or ./trt.sh [[-e] | [--empty]] start with empty file"
    echo "     or ./trt.sh [--testkey1]       start with inverse sort for key1"
    echo "     or ./trt.sh [--testkey2]       start with inverse sort for key2"
    echo "     or ./trt.sh [--testkey3]       start with inverse sort for key3"
    echo "     or ./trt.sh [[-n] | [--num] n] start with n record (n integer > 0)"
    echo "     or ./trt.sh                    normal start"
}

# test of an empty file
empty () {
    echo -n "" | ./splitfile.py --file -
}

# test of a file badly sorted for key1 - reversed order
testkey1 () {
    ./generate.py --num $1 | LC_ALL=C sort +1rn -2 +2n -3 +3n -4 +4n -5 | ./splitfile.py --gem "gem" --file -
}

# test of a file badly sorted for key2 - reversed order
testkey2 () {
    ./generate.py --num $1 | LC_ALL=C sort +1n -2 +2rn -3 +3n -4 +4n -5 | ./splitfile.py --gem "gem" --file -
}

# test of a file badly sorted for key3 - reversed order
testkey3 () {
    ./generate.py --num $1 | LC_ALL=C sort +1n -2 +2n -3 +3rn -4 +4n -5 | ./splitfile.py --gem "gem" --file -
}

### main

if [[ $1 == "" ]]; then
    treatment 500000
    exit
else
    case $1 in
        -h | --help )   usage
                        exit
                        ;;
        -e | --empty )  empty
                        exit
                        ;;
        --testkey1 )    testkey1 500000
                        exit
                        ;;
        --testkey2 )    testkey2 500000
                        exit
                        ;;
        --testkey3 )    testkey3 500000
                        exit
                        ;;
        -n | --num )    shift
                        if [[ $1 = +([0-9]) && $1 -ne 0 ]]; then
                            treatment $1
                            exit
                        else
                            echo "num is not a non zero positive integer"
                            usage
                            exit -1
                        fi
                        ;;
        * )             echo "unable to read parameters"
                        usage
                        exit -1
                        ;;
    esac
fi
