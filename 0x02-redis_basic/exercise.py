#!/usr/bin/env python3
"""
   working with redis
"""
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ Decorater that takes a single method and returns a callable """
    @wraps(method)
    def increment_key_value(self: Any, *args, **kwargs) -> str:
        """ Wraps store cache function and Increment the
            value associated with key every time store function is called
        """
        self._redis.incr(method.__qualname__)  # Increment key value
        return method(self, *args, **kwargs)
    return increment_key_value


def call_history(method: Callable) -> Callable:
    """ Decorator that store inputs and outputs of
        the function cache.store in a redis list
    """
    @wraps(method)
    def wrapper(self: Any, *args, **kwargs):
        """ Append input parameters of catch.store inside a list
            and append output of cache.store inside another list
        """
        # Appending the input parameter inside inputs redis list
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))

        return_value = method(self, *args)

        # Appending the return value of catch.store inside output redis list
        self._redis.rpush(f'{method.__qualname__}:outputs', return_value)
        return return_value
    return wrapper


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
    @call_history
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
        """ call appropirate method of conversion """
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

    def replay(self):
        """ Print number of times a method called with key and value """
        print("Catch.store was called {} times:".format(
            len(self.store.__qualname__)))
        inputs = self._redis.lrange("{}:inputs".format(
            self.store.__qualname__), 0, -1)
        outputs = self._redis.lrange("{}:outputs".format(
            self.store.__qualname__), 0, -1)
        input_output = list(zip(inputs, outputs))
        for key_value_pair in input_output:
            print("Cache.store(*{}) -> {}".format(
                key_value_pair[0].decode(
                    'utf-8'), (key_value_pair[1]).decode('utf-8')))
