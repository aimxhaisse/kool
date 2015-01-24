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
            d = json.loads(file)

    current = STATE_UNKNOWN
    entry = dict()

    with open(kconfig) as file:
        for line in file.readlines():
            if len(line) == 0 or line[0] == '#':
                continue
            m = re.match('^config ([^\s]+)$', line)
            if m:
                current = STATE_IN_CONFIG
                entry = dict()
                entry['name'] = m.group(1)
                continue
            if line == '\t---help---' or line == 'help':
                current = STATE_IN_HELP
                continue
            if current == STATE_IN_HELP:
                entry['help'] += line
                continue
            if state == STATE_UNKNOWN:
                continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parses a Kconfig and store its content to a JSON file.')
    parser.add_argument('kconfig')
    parser.add_argument('json')
    args = parser.parse_args()
    scan_kconfig(args.kconfig, args.json)
