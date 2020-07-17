# -*- coding: utf-8 -*-
# Based on:
# [0] http://stackoverflow.com/a/27517681/3420199
import mmap
import os
import subprocess

from itertools import takewhile
from itertools import repeat


def rawbigcount(filename):
    f = open(filename, 'rb')
    bufgen = takewhile(
        lambda x: x, (f.raw.read(1024*1024) for _ in repeat(None))
    )
    return sum( buf.count(b'\n') for buf in bufgen if buf )


def _make_gen(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024*1024)


def rawpycount(filename):
    f = open(filename, 'rb')
    f_gen = _make_gen(f.raw.read)
    return sum( buf.count(b'\n') for buf in f_gen )


# [1] https://gist.github.com/zed/0ac760859e614cd03652
def mapcount(filename):
    f = open(filename, "r+")
    buf = mmap.mmap(f.fileno(), 0)
    lines = 0
    readline = buf.readline
    while readline():
        lines += 1
    return lines


def simplecount(filename):
    lines = 0
    for line in open(filename):
        lines += 1
    return lines


def bufcount(filename):
    f = open(filename)
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.read  # loop optimization

    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)

    return lines


def wccount(filename):
    out = subprocess.Popen(
        ['wc', '-l', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    ).communicate()[0]
    return int(out.partition(b' ')[0])


def itercount(filename):
    return sum(1 for _ in open(filename, 'rbU'))


def opcount(fname):
    with open(fname) as f:
        for line_number, _ in enumerate(f, 1):
            pass
    return line_number


def kylecount(fname):
    return sum(1 for line in open(fname))


def clear_cache():
    """Clear disk cache on Linux."""
    os.system("sync ; sudo /bin/sh -c 'echo 3 > /proc/sys/vm/drop_caches'")