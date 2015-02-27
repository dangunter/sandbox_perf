# Sandbox performance testing

Author: Dan Gunter <dkgunter@lbl.gov>

This repository is for utility scripts for running sandbox performance
testing.

## Prerequisites

This code was written in Python 3.x, and may require minor modifications
to run under Python 2.x

You need access to a MongoDB database server. 

## Installation

Install using pip and setup.py

    # install package dependencies
    pip install -r requirements.txt
    # install local code
    python setup.py install
    
## Configuration

You can configure the connection with a JSON file, see `local.conf` for an example.

## Running

Scripts are in the `scripts` directory. They will be installed by the setup.py into
your PATH.

* add_sandbox.py - Add a sandbox, with fake values, to some percentage of
 records in the target collection.
* extract_queries.py - Extract, from the grepped logfiles, the MongoDB query that
can be re-executed.
* run_queries.py - Run queries (from extract_queries.py) on the target collection.

## Experiments

Using configuration file `local.conf` to connect to a MongoDB running on
my laptop:

    {"host": "localhost",
    "port": 27017,
    "database": "mg_core_dev",
    "collection": "materials"
    }

Run these commands:

    # clear out old sandboxes
    add_sandbox.py _ local.conf  --clear
    # add 5 'dang' sandboxes to 1% of the records
    # also adds empty sandbox sections to every record
    add_sandbox.py dang local.conf -n 5 -p 1
    # run queries
    run_queries.py 