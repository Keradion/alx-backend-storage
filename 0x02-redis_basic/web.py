#!/usr/bin/env python3
"""
   Implementing an expiring web cache and tracker
"""
import redis
import requests
from typing import Callable, Any
from functools import wraps

redis_client = redis.Redis()


def count_url(method: Callable) -> Callable:
    """
        Decorator to track how many times a URL accessed
        and cache the result for 10 sec with expiration.
        Track the frequency using "count:{url}" as a key.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """ """
        url = str(url)
        # Redis keys
        url_count_key = 'count:{}'.format(url)
        url_cache_key = '{}'.format(url)
        redis_client.incr(url_count_key)
        # Check if the URL html content is already in the cache
        html_content = redis_client.get(url_cache_key)
        if html_content:
            return html_content.decode('utf-8')
        # If the url html content is not in the cache, store it for 10 sec.
        html_content = method(url)
        redis_client.setex(url_cache_key, 10, (html_content))
        return html_content
    return wrapper


@count_url
def get_page(url: str) -> str:
    """ Fetch html content of a url using request and return it """
    html_page = requests.get(url)
    return html_page.text
