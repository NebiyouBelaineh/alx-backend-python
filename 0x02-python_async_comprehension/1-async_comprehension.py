#!/usr/bin/env python3
"""Coroutine that collects 10 random numbers using an async comprehension."""
import asyncio
import random
from typing import List


async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """Coroutine that collects 10 random numbers using an async comprehension.

    Returns:
        List[float, None]: _description_
    """
    return [res async for res in async_generator()]
