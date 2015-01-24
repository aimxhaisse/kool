#!/usr/bin/env bash

kernel=$1
json=$2

function scan-kconfigs
{
    for conf in $(find $kernel -name Kconfig)
    do
	./konfz/scripts/scan-kconfig.py $kernel $conf $json || exit
    done
}

scan-kconfigs
