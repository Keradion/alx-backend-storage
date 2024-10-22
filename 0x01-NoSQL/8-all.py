#!/usr/bin/env python3
""" List all documents in MongoDb collection """
from typing import List


def list_all(mongo_collection):
    """ Return all documents inside mongo_collection collection 
        otherwise return [] if no document in the collection 
    """
    try:
        return mongo_collection.find({})  #  Return all documents inside a collection
    except Exception:
        return []  #  Return empty list if no document in a collection 
