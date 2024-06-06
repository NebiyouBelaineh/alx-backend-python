#!/usr/bin/env python3
"""Module containing safely_get_value function."""
from typing import Any, Union, Mapping, TypeVar


T = TypeVar('T')


def safely_get_value(
                    dct: Mapping, key: Any,
                    default: Union[T, None] = None) -> Union[Any, T]:
    if key in dct:
        return dct[key]
    else:
        return default
