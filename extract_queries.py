#!/usr/bin/env python
"""
Extract MongoDB queries from a django-perf.log logfile
"""
__author__ = 'Dan Gunter <dkgunter@lbl.gov>'
__date__ = '2/23/15'

import argparse
import re
import sys
from urllib import parse

show_warnings = False

def warn(msg):
    if show_warnings:
        sys.stderr.write('* ' + msg + '\n')

def extract(infile, outfile):
    # queries with query= inside are pure Mongo gold
    expr = re.compile(r'query="query=(.*?)"')
    num = 0
    for line in infile:
        num += 1
        m = expr.search(line)
        if m is None:
            warn("Line {:d}: No query found".format(num))
            continue
        uquery = m.group(1)
        query = parse.unquote(uquery)
        msg = "{}\n".format(query)
        outfile.write(msg)

def main():
    global show_warnings
    p = argparse.ArgumentParser()
    p.add_argument('file', help="Input log file")
    p.add_argument('-o', '--output', dest="ofile", metavar="FILE", default=None,
                   help="Output file (default=stdout)")
    p.add_argument('-w', '--warnings', dest="warnings", action="store_true",
                   help="Show warnings for non-matching lines (default=False)")
    args = p.parse_args()
    infile, outfile = None, None
    try:
        infile = open(args.file, 'r')
        if args.ofile is None:
            outfile = sys.stdout
        else:
            outfile = open(args.ofile, 'w')
    except IOError as err:
        which = "input" if infile is None else "output"
        p.error("Error opening {} file: {}".format(which, err))
    if args.warnings:
        show_warnings = True
    extract(infile, outfile)


if __name__ == '__main__':
    sys.exit(main())
