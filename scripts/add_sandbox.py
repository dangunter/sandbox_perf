#!/usr/bin/env python
"""
Add some fake sandbox to existing materials collection.
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

def add(client, name, pct, num_sbx):
    """Add sandboxes to the MongoDB collection.

    Args:
       client (MongoClient): with .collection attribute
       name (str): Base name of sandbox
       pct (float): Percent chance that a given record will have new values added
       num_sbx (int): Number of sandboxes, named <name>_<#>, to add
    Return:
        (int) Number of records to which sandboxes were added.
    """
    prob = min(pct / 100.0, 1.0)
    changed, inserted, examined = 0, 0, 0

    cursor = client.collection.find({}, fields={'_id':1, SBX_KEY:1})
    count = cursor.count()

    update = lambda _id, sbxd: client.collection.update({'_id': _id},
        {'$set': {SBX_KEY: sbxd}}, upsert=False)

    progress(0, 0, count)

    for record in cursor:
        examined += 1
        r = random.random()
        if r > prob:
            # do not add to this record
            if SBX_KEY not in record:
                # add empty sandbox section
                update(record['_id'], [])
                inserted += 1  # but, don't count towards total
        else:
            # add to this record
            sbxd = record.get(SBX_KEY, [])
            for i in range(num_sbx):
                name_i = "{}_{:d}".format(name, i)
                sbxd.append({SBX_ID: name_i, 'e_above_hull': r + 0.01 * i})
            update(record['_id'], sbxd)
            inserted += 1
            changed += 1
        if inserted % 100 == 0:
            progress(inserted, examined, count)

    progress(inserted, examined, count, final=True)

    return changed

def progress(n, n2, total, final=False):
    term = '\n' if final else '        \r'
    msg = "inserted {:d} records ({:d} examined) / {:d} total"\
        .format(n, n2, total)
    sys.stderr.write(msg + term)
    sys.stderr.flush()

def clear(client):
    client.collection.update({}, {'$set': {SBX_KEY: []}})

def main():
    global show_warnings
    p = argparse.ArgumentParser()
    p.add_argument('name', help='Base sandbox name')
    p.add_argument('config', help="Database connection configuration file. "
                                  "The file is JSON, with the keys: database, collection, host, port")
    p.add_argument('--clear', action="store_true", dest="clear",
                   help="Clear all sandboxes and exit")
    p.add_argument('-n', '--num', dest='num', type=int, default=1,
                   help="Number of sandboxes to add. They will be named "
                        "sequentially: <name>_<#> (default=%(default)d)")
    p.add_argument('-p', '--percent', dest='pct', type=float, default=10.,
                   help="Percent of entries to add new sandbox to "
                        "(default=%(default)f)")
    args = p.parse_args()
    client = None
    try:
        config = json.load(open(args.config, 'r'))
        client = MongoClient(config)
    except ConnectionError as err:
        p.error("Error connecting to MongoDB: {}".format(err))
    except Exception as err:
        p.error("Error reading configuration file: {}".format(err))

    if args.clear:
        clear(client)
    else:
        add(client, args.name, args.pct, args.num)


if __name__ == '__main__':
    sys.exit(main())

