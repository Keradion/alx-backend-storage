#!/usr/bin/env python3
""" Update all topics of a school document """


def update_topics(mongo_collection, name, topics):
    """ Update a document in mongo_collection with name name to the
    value topics
    """
    # Filter to identify the document to be update
    query_filter = {'name': name}
    # Document key and new value to be update
    update_operation = {'$set': {'topics': topics}}
    # updating document ...
    mongo_collection.update_many(query_filter, update_operation)
