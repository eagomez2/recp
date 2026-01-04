import os
from contextlib import contextmanager
from typing import (
    Any,
    List
)


def make_list(x: Any) -> List[Any]:
    """If `x` is a single element, turns it into a `list` of one element.

    Args:
        x (Any): Element(s) to be returned as a `list`.

    Returns:
        (list): `x` as a `list`.
    """
    return [x] if not isinstance(x, list) and x is not None else x


@contextmanager
def temp_env(merge: dict = {}):
    old_env = os.environ.copy()
    
    try:
        os.environ.update({k: str(v) for k, v in merge.items()})
        yield
    
    finally:
        os.environ.clear()
        os.environ.update(old_env)
