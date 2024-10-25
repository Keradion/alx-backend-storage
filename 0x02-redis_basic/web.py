#!/usr/bin/env python3
"""
   Catch a web page response 
"""
import redis
import requests
from typing import Callable, Any
from functools import wraps

def track_get_page(method: Callable) -> Callable:
    """ Returns wrapper """
    @wraps(method)
    def wrapper(self: Any, *args, **kwargs) -> str:
        self._redis.incr(f'count:{args[0]}')
        cached_page = self._redis.get(f'count:{args[0]}')
        if cached_page:
            return chached_page.decode('utf-8')

        result = method(self, *args, **kwargs)
        self._redis.set(f'{arg[0]}', result, 10)
    return wrapper

class Cache:
    """ Cache class """
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @track_get_page
    def get_page(self, url: str) -> str:
        """ 
            Perform an http request and return the body
            of the response
        """
        html_page = requests.get(url)
        return html_page.text
