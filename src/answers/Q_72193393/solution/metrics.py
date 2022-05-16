

from typing import Tuple
from typing import Iterable, Optional, Callable, List

import pandas as pd
import numpy as np


__all__ = [
    "myFunc2",
]


def myFunc(params):
    """myFunc metric."""
    global df # define as a global variable
    (ev, bv, vc, dv) = params
    df['Number'] = np.where(df['Dividend2'] <= vc, 1, 0) \
                    + np.where(df['EV2'] <= dv, 1, 0)
    df['Return'] =  np.where(
        df['EV'] <= ev, 0, np.where(
            df['Probability'] >= bv, 0, df['Number'] * df['Dividend'] - (vc + dv)
        )
    )
    return -1 * (df['Return'].sum())


def myFunc2(params: List[Tuple[float, float]]) -> float:
    """myFunc metric v2 with lesser steps."""
    global df # define as a global variable
    (ev, bv, vc, dv) = params
    df['Number'] = (df['Dividend2'] <= vc) * 1 + (df['EV2'] <= dv) * 1
    df['Return'] =  (
        (df['EV'] > ev) 
        * (df['Probability'] < bv) 
        * (df['Number'] * df['Dividend'] - (vc + dv))
    )
    return -1 * (df['Return'].sum())
