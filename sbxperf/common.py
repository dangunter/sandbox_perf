"""
Some common stuff
"""
__author__ = 'Dan Gunter <dkgunter@lbl.gov>'
__date__ = '2/23/15'

import pymongo

ConnectionError = pymongo.errors.ConnectionFailure

class MongoClient(pymongo.MongoClient):
    """JSON-configurable client.
    """
    def __init__(self, cfg):
        host = cfg.get('host', 'localhost')
        port = int(cfg.get('port', 27017))
        pymongo.MongoClient.__init__(self, host, port)
        self.database, self.collection = None, None
        if 'database' in cfg:
            self.db = self[cfg['database']]
            if 'user' in cfg and 'password' in cfg:
                ok = self.db.authenticate(cfg['user'], cfg['password'])
                if not ok:
                    raise ConnectionError("Failed to authenticate. "
                                          "user={user} password={password}".format(
                        **cfg))
            if 'collection' in cfg:
                self.collection = self.db[cfg['collection']]

