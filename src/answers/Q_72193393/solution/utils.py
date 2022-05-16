import pandas as pd
import numpy as np
from scipy import optimize

from solution import Config, CustomMetrics

PARAM_NAMES = Config.PARAM_NAMES
DEFAULT_METRIC_FUNC = Config.DEFAULT_METRIC_FUNC

def generate_data() -> pd.DataFrame:
    """Generate dummy data."""
    cols = {
        'Dividend2': [9390, 7448, 177], 
        'Probability': [341, 376, 452], 
        'EV': [0.53, 0.60, 0.55], 
        'Dividend': [185, 55, 755], 
        'EV2': [123, 139, 544],
    }

    df = pd.DataFrame(cols)
    
    return df


def make_param_grid(
        bounds: List[Tuple[float, float]], 
        param_names: Optional[List[str]]=None, 
        num_points: int=10, 
        as_dict: bool=True,
    ) -> Union[pd.DataFrame, Dict[str, List[float]]]:
    """
    Create parameter search space.

    Example:
    
        grid = make_param_grid(bounds=b1, num_points=10, as_dict=True)
    
    """
    if param_names is None:
        param_names = PARAM_NAMES # ["ev", "bv", "vc", "dv"]
    bounds = np.array(bounds)
    grid = np.linspace(start=bounds[:,0], 
                       stop=bounds[:,1], 
                       num=num_points, 
                       endpoint=True, 
                       axis=0)
    grid = pd.DataFrame(grid, columns=param_names)
    if as_dict:
        grid = grid.to_dict()
        for k,v in grid.items():
            grid.update({k: list(v.values())})
    return grid


def make_hiplot(search_grid: pd.DataFrame, num_smallest: Optional[int]=None, column: str="returns"):
    """Make  hiplot (parallel coordinate) plot."""
    search_grid = search_grid if (num_smallest is None) else (
        search_grid
            .loc[ sg.search_grid[column]
                    .nsmallest( n=np.abs(num_smallest), 
                                keep="first")
                    .index]
    )
    fig = px.parallel_coordinates(
        search_grid, 
        color=column, 
        color_continuous_scale=px.colors.diverging.Tealrose,
        # color_continuous_midpoint=2,
    )
    fig.show()
    return fig


# b1 = [(0.2,4), (300,600), (0,1000), (0,1000)]
# start = [0.2, 600, 1000, 1000]
# result = optimize.minimize(fun=myFunc, bounds=b1, x0=start)
# print(result)