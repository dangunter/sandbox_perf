#!/usr/bin/env python
"""
Check on fake sandboxes that were added with `add_sandbox`.
"""
__author__ = 'Dan Gunter <dkgunter@lbl.gov>'
__date__ = '2/23/15'

import argparse
import json
import random
import sys
import time

from sbxperf.common import ConnectionError, MongoClient

# sbxd: [{id: 'jcesr', e_above_hull: 1}, {id: 'mp', e_above_hull: 1.1}]
# db.materials.ensureIndex({'sbxd.id': 1, 'sbxd.e_above_hull': 1, ...})

SBX_KEY = 'sbxd'
SBX_ID = 'id'


def check(client, name):
    any_sandbox = (name == '*')
    cursor = client.collection.find({}, {'_id':1, SBX_KEY:1})

    total = cursor.count()
    rec_count, sbx_count, name_count = 0, 0, 0

    for record in cursor:
        rec_count += 1
        if (rec_count % 100) == 0:
            print("{:d} / {:d}      ".format(rec_count, total), end='\r')
            sys.stdout.flush()
        if SBX_KEY in record:
            sbx_count += 1
            if not any_sandbox:
                for sbx in record[SBX_KEY]:
                    if sbx['id'].startswith(name):
                        name_count += 1
                        break
    print(" Done")
    if any_sandbox:
        print("{:d} records, {:d} with sandboxes".format(rec_count, sbx_count))
    else:
        print("{:d} records, {:d} with sandboxes {:d} with the '{}' sandbox"
              .format(rec_count, sbx_count, name_count, name))


def main():
    global show_warnings
    p = argparse.ArgumentParser()
    p.add_argument('config', help="Database connection configuration file. "
                                  "The file is JSON, with the keys: database, collection, host, port")
    p.add_argument('-n', '--name', dest='name', default='*',
                   help='Base sandbox name (default=*, meaning any)')
    args = p.parse_args()
    client = None
    try:
        config = json.load(open(args.config, 'r'))
        client = MongoClient(config)
    except ConnectionError as err:
        p.error("Error connecting to MongoDB: {}".format(err))
    except Exception as err:
        p.error("Error reading configuration file: {}".format(err))

    check(client, args.name)


if __name__ == '__main__':
    sys.exit(main())

