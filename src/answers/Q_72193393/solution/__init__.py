from solution import metrics as CustomMetrics
from solution import utils
from solution.config import Config

try:
    from importlib import metadata
except ImportError:  # for Python<3.8
    import importlib_metadata as metadata


__title__ = __name__
__version__ = metadata.version(__title__)  # type: ignore

__all__ = [
    "CustomMetrics",
    "Config",
    "utils",
]