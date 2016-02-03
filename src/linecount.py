# -*- encoding: utf-8 -*-
# Based on:
# [0] http://stackoverflow.com/a/27517681/3420199


# import time
import mmap
import os
# import random
import subprocess
# import sys

# from collections import defaultdict
# from timeit import default_timer as timer
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


# ------------------------------------------------------------------------------
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


# try:
#     # http://chris-lamb.co.uk/projects/python-fadvise/
#     from fadvise import sequential, normal

#     def fadvcount(fname):
#         sequential(fname)
#         c = bufcount(fname)
#         normal(fname)
#         return c

# except ImportError:
#     import warnings
#     warnings.warn(
#         'Can\'t import fadvise: fadvcount() will be unavailable',
#         UserWarning
#     )


def clear_cache():
    """Clear disk cache on Linux."""
    os.system("sync ; sudo /bin/sh -c 'echo 3 > /proc/sys/vm/drop_caches'")


# def main():
#     counts = defaultdict(list)

#     if '--clear-cache' in sys.argv:
#         sys.argv.remove('--clear-cache')
#         do_clear_cache = True
#     else:
#         do_clear_cache = False

#     filename = sys.argv[1] if len(sys.argv) > 1 else "big.txt"
#     for i in range(3):
#         for func in (f
#                      for n, f in globals().items()
#                      if n.endswith('count') and hasattr(f, '__call__')):
#             if do_clear_cache:
#                 clear_cache()
#             start_time = timer()
#             # http://norvig.com/big.txt
#             if filename == 'big.txt':
#                 # 128457 1095695 6488666 big.txt
#                 assert func(filename) == 128457
#             else:
#                 func(filename)
#             counts[func].append(timer() - start_time)

#     timings = {}
#     for key, vals in counts.items():
#         timings[key.__name__] = sum(vals) / float(len(vals)), min(vals)
#     width = max(len(n) for n in timings) + 1
#     print("%s %s %s %s" % (
#         "function".ljust(width),
#         "average, s".rjust(11),
#         "min, s".rjust(7),
#         "ratio".rjust(6)))
#     absmin_ = min(x[1] for x in timings.values())
#     for name, ( av, min_) in sorted(timings.items(), key=lambda x: x[1][1]):
#         print("%s %11.2g %7.2g %6.2f" % (
#             name.ljust(width), av, min_, min_/absmin_))


# if __name__ == '__main__':
#     main()
