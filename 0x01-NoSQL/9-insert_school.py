#!/usr/bin/env python3
""" Insert a new document in a collection """


def insert_school(mongo_collection, **kwargs):
    """ Inserts key value pairs or new document
        into collection mongo_collection
    """
    document = {}  # Hold filed and value of the document to be insert

    for key, value in kwargs.items():
        document[key] = value

    document_id = mongo_collection.insert_one(document)  # Insert the document
    return document_id.inserted_id  # Retrun new document objectId
