# -*- coding: utf-8 -*-

import pymongo
from settings import MONGODB_CONFIG
from pymongo.son_manipulator import AutoReference, NamespaceInjector


class Database(object):
    def __init__(self):
        conn = pymongo.Connection("mongodb://%s" % MONGODB_CONFIG['HOST'],
                                  port=MONGODB_CONFIG['PORT'],
                                  #replicaSet='audit',
                                  #w=2, j=True,
                                  network_timeout=15)

        self.db = conn.diggit
        self.db.add_son_manipulator(AutoReference(self.db))

    def insert(self, table, documents):
        return self.db[table].insert(documents)

    def query(self, table, parameters, sort, offset, limit, fields=None):
        cursor = self.db[table].find(parameters, fields)\
            .skip(offset).limit(limit)
        cursor.sort(sort, pymongo.DESCENDING)
        return cursor

    def get_count(self, table, parameters):
        return self.db[table].find(parameters).count()

    def get_id(self, table):
        value = self.db["ids"].find_and_modify(
            {"name": table}, {"$inc": {"value": 1}}, new=True, upsert=True)
        return value["value"]

    def find_one(self, table, parameters):
        return self.db[table].find_one(parameters)

    def update(self, table, parameters, update, safe=True):
        return self.db[table].update(parameters, update, safe)

    def dereference(self, dbref):
        return self.db.dereference(dbref)

    def remove(self, table, parameters):
        self.db[table].remove(parameters)

