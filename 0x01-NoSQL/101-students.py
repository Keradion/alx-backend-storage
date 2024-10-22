#!/usr/bin/env python3
"""
   a Python function that returns all students sorted by average score
"""


def top_students(mongo_collection):
    """ Sort and return student documents by score from mongo_collection """
    for student in (mongo_collection).find({}):
        total_score = 0
        count = 0
        for topic in student.get('topics'):
            total_score = total_score + topic.get('score')
            count += 1
        mongo_collection.update_one({'_id': student.get(
            '_id')}, {'$set': {'averageScore': total_score / count}})

    return list(mongo_collection.find().sort('averageScore', -1))
