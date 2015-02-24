# Sandbox performance testing

Author: Dan Gunter <dkgunter@lbl.gov>

This repository is for utility scripts for running sandbox performance
testing.

# Prerequisites

This code was written in Python 3.x, and may require minor modifications
to run under Python 2.x

You need access to a MongoDB database server. You can configure the connection;
see `local.conf` for an example.

# Installation

Install using pip and setup.py

    # install package dependencies
    pip install -r requirements.txt
    # install local code
    python setup.py install
    
# Python code

Shared code is in the `sbxperf` package.

# Scripts

Scripts are in the `scripts` directory. They will be installed by the setup.py into
your PATH.

* add_sandbox.py - Add a sandbox, with fake values, to some percentage of
 records in the target collection.
* extract_queries.py - Extract, from the grepped logfiles, the MongoDB query that
can be re-executed.
* run_queries.py - Run queries (from extract_queries.py) on the target collection.


