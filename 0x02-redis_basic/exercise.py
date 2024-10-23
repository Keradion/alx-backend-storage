#!/usr/bin/env python3
""" Writing strings to Redis database key value pair
"""
import redis
import uuid
from typing import Union


class Cache:
    """
       Cache class to initialize and manage Redis instance
    """
    def __init__(self) -> None:
        """
           Create Redis instance and clear existing key value pairs
        """
        # Redis instance db __redis created
        self.__redis = redis.Redis()
        # Delete all keys in the current Redis instance db __redis
        self.__redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
            Takes data argument and generate a random key
            store the data in redis using the key and return the key
        """
        # Generating a random key using uuid
        random_key = str(uuid.uuid4())

        # Storing the data on redis db using random_key as key
        self.__redis.set(random_key, data)

        return random_key

    def get(self, key: str, fn: callable=None) -> any:
        # Fetching the value associated with key in redis
        value = self.__redis.get(key)
        if not value:
            return 
        if fn is int:
            self.get_int(value)
        if fn is str:
            self.get_str(value)


    def get_str(self, value: byte) -> str:
        """
           Converts byte to string 
        """
        return value.decode('utf-8')

    def get_int(self, value: byte) -> int:
        """
           Converts byte to integer
        """
        return int(value)

