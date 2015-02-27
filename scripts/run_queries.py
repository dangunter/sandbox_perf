#!/usr/bin/env python
"""
Run a bunch of queries, line-separated in a text file.
As in, the output of the extract_queries.py script.
"""
__author__ = 'Dan Gunter <dkgunter@lbl.gov>'
__date__ = '2/23/15'

import argparse
import operator
import json
import sys
import time

import pymongo

from sbxperf.common import ConnectionError, MongoClient

def do_queries(infile, client):
    start_time = time.time()
    timings = []
    for line in infile:
        spec = json.loads(line.strip())
        qt0 = time.time()
        cursor = client.collection.find(spec, fields={'_id': 1})
        sys.stderr.write("-----------------------------------------------\n")
        sys.stderr.write("Query: {}\n".format(spec))
        sys.stderr.write("Plan: {}\n".format(json.dumps(cursor.explain(), indent=2)))
        n = cursor.count()
        qt = time.time() - qt0
        sys.stderr.write(".")
        sys.stderr.flush()
        timings.append((spec, qt, n))
    end_time = time.time()
    sys.stderr.write("\n")
    return timings, start_time - end_time

def print_timings(ofile, individual, total):
    longest_first = sorted(individual, key=operator.itemgetter(1), reverse=True)
    for timing in longest_first:
        ofile.write("{:6.1f}s   n={:d}  {}\n".format(timing[1], timing[2], timing[0]))
    ofile.write("\n" + "=" * 50)
    ofile.write("\n{:6.1f}s   Total, including loop overhead".format(total))

def main():
    global show_warnings
    p = argparse.ArgumentParser()
    p.add_argument('file', help="Input query file file")
    p.add_argument('config', help="Database connection configuration file. "
        "The file is JSON, with the keys: database, collection, host, port")
    p.add_argument('-o', '--output', dest="ofile", metavar="FILE", default=None,
                   help="Output file for performance results (default=stdout)")
    p.add_argument('-w', '--warnings', dest="warnings", action="store_true",
                   help="Show warnings for non-matching lines (default=False)")
    args = p.parse_args()
    which, infile, client, outfile = "", None, None, None
    try:
        which = "input"
        infile = open(args.file, 'r')
        which = "output"
        if args.ofile is None:
            outfile = sys.stdout
        else:
            outfile = open(args.outfile, 'w')
        which = "configuration"
        config = json.load(open(args.config, 'r'))
        client = MongoClient(config)
    except IOError as err:
        p.error("Error opening {} file: {}".format(which, err))
    if args.warnings:
        show_warnings = True
    print_timings(outfile, *do_queries(infile, client))


if __name__ == '__main__':
    sys.exit(main())

