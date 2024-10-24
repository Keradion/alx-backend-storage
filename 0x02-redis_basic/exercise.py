#!/usr/bin/env python3
""" Writing strings to Redis database key value pair
"""
import redis
import uuid
from typing import Union, Callable, Ang
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """ Decorater that takes a single method and returns a callable """
    @wraps(method)
    def increment_key_value(self: Any, *args, **kwargs) -> str:
        """ Wraps store cache function and Increment the value associated with key
            every time store function is called
        """
        self._redis.incr(method.__qualname__)  # Increment the value of the key by 1
        return function_store(self, *args, **kwargs)
    return increment_key_value

class Cache:
    """
       Cache class to initialize and manage Redis instance
    """
    def __init__(self) -> None:
        """
           Create Redis instance and clear existing key value pairs
        """
        # Redis instance db __redis created
        self._redis = redis.Redis()
        # Delete all keys in the current Redis instance db __redis
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
            Takes data argument and generate a random key
            store the data in redis using the key and return the key
        """

        # Generating a random key using uuid
        random_key: str = str(uuid.uuid4())

        # Storing the data on redis db using random_key as key
        self._redis.set(random_key, data)

        return random_key
    
    def get(self, key: str, fn: callable = None) -> Any:
        # Fetching the value associated with key in redis
        value: str = self._redis.get(key)
        if not value:
            return 
        if fn is int:
            return self.get_int(value)
        if fn is str:
            return self.get_str(value)
        return value


    def get_str(self, value: bytes) -> str:
        """
           Converts byte to string 
        """
        return value.decode('utf-8')

    def get_int(self, value: bytes) -> int:
        """
           Converts byte to integer
        """
        return int(value)

