#!/usr/bin/env python3
"""
   Implementing an expiring web cache and tracker
"""
import redis
import requests
from typing import Callable, Any
from functools import wraps


def count_url(method: Callable) -> Callable:
    """
        Decorator to track how many times a URL accessed
        and cache the result for 10 sec with expiration.
        Track the frequency using "count:{url}" as a key.
    """
    @wraps(method)
    def wrapper(url: str) -> Callable:
        """ """
        url = str(url)
        redis_client = redis.Redis()
        url_count_key = 'count:{}'.format(url)
        url_cache_key = '{}'.format(url)
        redis_client.incr(url_count_key)
        
        html_content = method(url)
        # Check if the URL html content is already in the cache
        url_exist = redis_client.get(url_cache_key)

        # If the url html content is not in the cache, store it for 10 sec.
        if not url_exist:
            redis_client.setex(url_cache_key, 10, html_content)
            print(redis_client.ttl(url_cache_key))
        return html_content
    return wrapper

 



@count_url
def get_page(url: str) -> str:
    """ Fetch html content of a url using request and return it """
    html_page = requests.get(url)
    return html_page.content


if __name__ == '__main__':
    result  = get_page('http://slowwly.robertomurray.co.uk')
    print(result)

