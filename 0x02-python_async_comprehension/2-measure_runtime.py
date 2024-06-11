#!/usr/bin/env python3
"""Coroutine that executes async_comprehension method four times in parallel
using async.gather."""
import asyncio
import time


async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """Measuers the runtime of async_comprehension four times in parallel"""

    start = time.perf_counter()

    coroutines = [async_comprehension() for _ in range(4)]
    batch = await asyncio.gather(*coroutines)

    end = time.perf_counter()
    return (end - start)
