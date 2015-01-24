#!/usr/bin/env python

"""
This script is not an efficient implementation, but it is simple
enough and we don't care that much about about efficiency here.

This idea is that for each Kconfig in the kernel tree, we iterate on
each ARCH (since some configs are arch dependent and we need to
specify an ARCH to iter with kconfiglib); we populate a JSON file
which is entirely rewritten upon each iteration.
"""

import kconfiglib
import argparse
import json
import os
import os.path
import re


def scan_kernel_version(kdir):
    """
    Returns the kernel version.
    """
    version = None
    patch = None
    sub = None
    with open('{0}/Makefile'.format(kdir)) as makefile:
        for line in makefile.readlines():
            m = re.match('VERSION = ([0-9]+).*', line)
            if m:
                version = m.group(1)
                continue
            m = re.match('PATCHLEVEL = ([0-9]+).*', line)
            if m:
                patch = m.group(1)
                continue
            m = re.match('SUBLEVEL = ([0-9]+).*', line)
            if m:
                sub = m.group(1)
                continue
            if version and patch and sub:
                break    
    return '{0}.{1}.{2}'.format(version, patch, sub)


def scan_archs(kdir):
    """
    Returns a list of available archs.
    """
    archs = []
    arch_dir = '{0}/arch'.format(kdir)
    for arch in os.listdir(arch_dir):
        full_path = '{0}/{1}'.format(arch_dir, arch)
        if os.path.isdir(full_path):
            archs.append(arch)
    return archs


def arch_to_src_arch(arch):
    """
    These conversion are based on Linux' main makefile.
    """
    if arch == 'i386':
        return 'x86'
    if arch == 'x86_64':
        return 'x86'
    if arch == 'sparc32':
        return 'sparc'
    if arch == 'sparc64':
        return 'sparc'
    if arch == 'sh64':
        return 'sh'
    if arch == 'tilepro':
        return 'tile'
    if arch == 'tilegx':
        return 'tile'
    return arch


def scan_kconfig(kdir, kconfig, result_file):
    d = dict()

    if os.path.exists(result_file):
        with open(result_file) as file:
            d = json.load(file)

    os.environ['KERNELVERSION'] = scan_kernel_version(kdir)
    for arch in scan_archs(kdir):
        os.environ['ARCH'] = arch
        os.environ['SUBARCH'] = arch
        os.environ['SRCARCH'] = arch_to_src_arch(arch)
        for item in kconfiglib.Config(kconfig, base_dir=kdir).get_top_level_items():
            try:
                name = item.get_name()
                if name not in d:
                    entry = dict()
                    entry['value'] = item.get_value()
                    entry['help'] = item.get_help()
                    d[name] = entry
            except:
                pass

    with open(result_file, 'w+') as file:
        file.write(json.dumps(d))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parses a Kconfig and store its content to a JSON file.')
    parser.add_argument('kdir')
    parser.add_argument('kconfig')
    parser.add_argument('json')
    args = parser.parse_args()
    try:
        scan_kconfig(args.kdir, args.kconfig, args.json)
    except:
        pass
