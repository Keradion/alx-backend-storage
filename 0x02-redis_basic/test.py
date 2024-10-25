#!/usr/bin/env python3
""" Main file """
from typing import Callable
Cache = __import__('exercise').Cache
cache = Cache()

inputs = cache.replay()
print(inputs)
