from dataclasses import dataclass

from solution import metrics as sm
from solution.dtypes import ParamNamesType, BoundsItemType

@dataclass
class Config:
    PARAM_NAMES: ParamNamesType = ["ev", "bv", "vc", "dv",]
    DEFAULT_METRIC_FUNC: Callable = sm.myFunc2
    PARAM_BOUNDS: List[BoundsItemType] = \
        [(0.2, 4), (300, 600), (0, 1000), (0, 1000)]
