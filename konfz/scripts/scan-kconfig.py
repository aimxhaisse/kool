#!/usr/bin/env python

import argparse
import json
import os.path
import enum
import re

STATE_IN_CONFIG = 'in_config'
STATE_IN_HELP = 'in_help'
STATE_UNKNWON = 'unknown'

def scan_kconfig(kconfig, json):
    d = dict()

    if os.path.exists(json):
        with open(json) as file:
            d = json.load(file)

    current = STATE_UNKNOWN
    entry = dict()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parses a Kconfig and store its content to a JSON file.')
    parser.add_argument('kconfig')
    parser.add_argument('json')
    args = parser.parse_args()
    scan_kconfig(args.kconfig, args.json)
