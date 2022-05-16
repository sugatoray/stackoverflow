import warnings
from functools import partial
from typing import Iterable, Optional, Callable, List

import pandas as pd
import numpy as np
import optuna
from tqdm.notebook import tqdm

from solution import Config, CustomMetrics

warnings.filterwarnings("ignore", category=optuna.exceptions.ExperimentalWarning)
optuna.logging.set_verbosity(optuna.logging.WARNING)

PARAM_NAMES = Config.PARAM_NAMES
DEFAULT_METRIC_FUNC = Config.DEFAULT_METRIC_FUNC


def objective(trial, 
              bounds: Optional[Iterable]=None, 
              func: Optional[Callable]=None, 
              param_names: Optional[List[str]]=None):
    """Objective function, necessary for optimizing with optuna."""
    if param_names is None:
        param_names = PARAM_NAMES
    if (bounds is None):
        bounds = ((-10, 10) for _ in param_names)
    if not isinstance(bounds, dict):
        bounds = dict((p, (min(b), max(b))) 
                        for p, b in zip(param_names, bounds))
    if func is None:
        func = DEFAULT_METRIC_FUNC

    params = dict(
        (p, trial.suggest_float(p, bounds.get(p)[0], bounds.get(p)[1])) 
        for p in param_names        
    )
    # x = trial.suggest_float('x', -10, 10)
    return func((params[p] for p in param_names))


def optimize(objective: Callable, 
             sampler: Optional[optuna.samplers.BaseSampler]=None, 
             func: Optional[Callable]=None, 
             n_trials: int=2, 
             study_direction: str="minimize",
             study_name: Optional[str]=None,
             formatstr: str=".4f",
             verbose: bool=True):
    """Optimizing function using optuna: creates a study."""
    if func is None:
        func = DEFAULT_METRIC_FUNC
    study = optuna.create_study(
        direction=study_direction, 
        sampler=sampler, 
        study_name=study_name)
    study.optimize(
        objective, 
        n_trials=n_trials, 
        show_progress_bar=True, 
        n_jobs=1,
    )
    if verbose:
        metric = eval_metric(study.best_params, func=myFunc2)
        msg = format_result(study.best_params, metric, 
                            header=study.study_name, 
                            format=formatstr)
        print(msg)
    return study


def format_dict(d: Dict[str, float], format: str=".4f") -> Dict[str, float]:
    """
    Returns formatted output for a dictionary with 
    string keys and float values.
    """
    return dict((k, float(f'{v:{format}}')) for k,v in d.items())


def format_result(d: Dict[str, float], 
                  metric_value: float, 
                  header: str='', 
                  format: str=".4f"): 
    """Returns formatted result."""
    msg = f"""Study Name: {header}\n{'='*30}
    
    ✅ study.best_params: \n\t{format_dict(d)}
    ✅ metric: {metric_value} 
    """
    return msg


def study_contour_plot(study: optuna.Study, 
                       params: Optional[List[str]]=None, 
                       width: int=560, 
                       height: int=500):
    """
    Create contour plots for a study, given a list or 
    tuple of two parameter names.
    """
    if params is None:
        params = ["dv", "vc"]
    fig = optuna.visualization.plot_contour(study, params=params)
    fig.update_layout(
        title=f'Contour Plot: {study.study_name} ({params[0]}, {params[1]})', 
        autosize=False,
        width=width, 
        height=height,
        margin=dict(l=65, r=50, b=65, t=90))
    fig.show()


if __name__ == "__main__":

    # bounds = [(0.2, 4), (300, 600), (0, 1000), (0, 1000)]
    bounds = Config.PARAM_BOUNDS
    param_names = PARAM_NAMES # ["ev", "bv", "vc", "dv",]
    pobjective = partial(objective, bounds=bounds)

    # Create an empty dict to contain 
    # various subsequent studies.
    studies = dict()
