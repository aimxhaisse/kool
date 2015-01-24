#!/usr/bin/env bash

kernel=$1

function scan-kconfigs
{
    confs=$(find $kernel -name Kconfig)
    for c in $conf
    do
	echo $c
    done
}

scan-kconfigs
