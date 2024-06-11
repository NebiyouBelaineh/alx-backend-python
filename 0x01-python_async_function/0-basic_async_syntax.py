#!/usr/bin/env python3
"""Asynchronous coroutine"""

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """Asynchronously wait for a random time between 0 and max_delay

    Args:
        max_delay (int, optional): delay time in seconds. Defaults to 10.

    Returns:
        float: delay time in seconds
    """
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
