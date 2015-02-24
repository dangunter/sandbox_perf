#!/usr/bin/env python
"""
Add some fake sandbox to existing materials collection.
"""
__author__ = 'Dan Gunter <dkgunter@lbl.gov>'
__date__ = '2/23/15'

import argparse
import json
import sys
import time

from sbxperf.common import ConnectionError, MongoClient

# sbxd: [{id: 'jcesr', e_above_hull: 1}, {id: 'mp', e_above_hull: 1.1}]
# db.materials.ensureIndex({'sbxd.id': 1, 'sbxd.e_above_hull': 1, ...})

def add(client, name, pct):
    pass

def main():
    global show_warnings
    p = argparse.ArgumentParser()
    p.add_argument('name', help='Sandbox name')
    p.add_argument('config', help="Database connection configuration file. "
                                  "The file is JSON, with the keys: database, collection, host, port")
    p.add_argument('-p', '--percent', dest='pct', type=int, default=10,
                   help="Percent of entries to add new sandbox to "
                        "(default=%(default)d)")
    args = p.parse_args()
    client = None
    try:
        config = json.load(open(args.config, 'r'))
        client = MongoClient(config)
    except ConnectionError as err:
        p.error("Error connecting to MongoDB: {}".format(err))
    except Exception as err:
        p.error("Error reading configuration file: {}".format(err))
    add(client, args.name, args.pct)


if __name__ == '__main__':
    sys.exit(main())

