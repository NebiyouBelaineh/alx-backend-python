#!/usr/bin/env python3

"""Module for printing the correct output of the wait_n coroutine"""

import asyncio
from typing import List


wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int = 10) -> List[float]:
    """Asynchronously wait for n random time between 0 and max_delay
    and return a sorted list of the delays

    Args:
        n (int): _description_
        max_delay (int, optional): _description_. Defaults to 10.

    Returns:
        List[float]: _description_
    """
    delay = []
    for _ in range(n):
        delay += [await wait_random(max_delay)]
    return sorted(delay)
