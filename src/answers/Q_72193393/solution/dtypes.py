from typing import (
    Dict, List, Tuple, 
    Union, Optional, Any, 
    Iterable, Callable,
)


__all__ = [
    "BoundsItemType",
    "ParamNamesType",
    "BoundsItemsDictType",
]


BoundsItemType = Tuple[float, float]
ParamNamesType = List[str]
BoundsItemsDictType = Dict[str, BoundsItemType]
