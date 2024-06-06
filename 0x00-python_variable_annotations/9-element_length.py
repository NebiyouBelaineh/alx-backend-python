#!/usr/bin/env python3
"""Module containing a function returs a list of tuples
containing the index and the length of the element."""
from typing import Tuple, List, Sequence, Iterable


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    return [(i, len(i)) for i in lst]
