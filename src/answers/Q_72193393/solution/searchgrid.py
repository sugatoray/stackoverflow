import gc
from typing import (
    Dict, List, Tuple, 
    Union, Optional, Any, 
    Iterable, Callable,
)

from tqdm.notebook import tqdm
# from tqdm.auto import tqdm  # for notebooks
# source: https://stackoverflow.com/questions/18603270/progress-indicator-during-pandas-operations

from solution import Config, CustomMetrics
from solution import utils as U
from solution.dtypes import (
    ParamNamesType, 
    BoundsItemType, 
    BoundsItemsDictType,
)

PARAM_NAMES = Config.PARAM_NAMES
DEFAULT_METRIC_FUNC = Config.DEFAULT_METRIC_FUNC

# PARAM_NAMES: ParamNamesType = ["ev", "bv", "vc", "dv",]
# DEFAULT_METRIC_FUNC: Callable = myFunc2

def eval_metric(params: Dict[str, float], 
                func: Optional[Callable]=None, 
                param_names: Optional[ParamNamesType]=None) -> float:
    """
    Evaluate a metric with a parameter-dictionary (``param``) 
    and a function (``func``).
    """
    if param_names is None:
        param_names = PARAM_NAMES
    if func is None:
        func = DEFAULT_METRIC_FUNC
    return func((params[p] for p in param_names))


def prepare_bounds(
        bounds: List[BoundsItemType], 
        param_names: Optional[ParamNamesType]=None
    ) -> BoundsItemsDictType:
    """Prepare bounds from a List of Tuples to."""
    if param_names is None:
        param_names = PARAM_NAMES
    if not isinstance(bounds, dict):
        bounds = dict((p, (min(b), max(b))) 
                        for p, b in zip(param_names, bounds))
    return bounds


class SearchGrid:
    """SearchGrid class."""

    param_grid: pd.DataFrame
    search_grid: pd.DataFrame
    target_column: str

    def __init__(self, bounds: BoundsItemsDictType):
        """Instatiate SearchGrid with parameter bounds."""
        self.bounds = bounds        

    def __repr__(self):
        return f"{self.__class__.__name__} class"

    def create_param_grid(self, num_points: int=10, inplace: bool=True):
        """Create parameter grid with values from parameter bounds."""
        self.param_grid = pd.DataFrame(
            dict(
                (k, np.linspace(start=low, stop=high, 
                                num=num_points, endpoint=True)
                ) 
                for k, (low, high) in bounds.items()
            )
        )
        if inplace:
            return self        

    def create_search_grid(self,
            param_grid: Optional[pd.DataFrame]=None, 
            verbose: bool=True,
            inplace: bool=False,
        ):
        """Create search grid with values from parameter grid."""
        if param_grid is None:
            param_grid = self.param_grid.copy()
        nrows, ncols = param_grid.shape

        search_grid = []

        with tqdm(total = nrows * ncols, desc="Creating...") as pbar:
            for ev in param_grid["ev"]:
                for bv in param_grid["bv"]:
                    for vc in param_grid["vc"]:
                        for dv in param_grid["dv"]:
                            search_grid.append(
                                {"ev": ev, "bv": bv, "vc": vc, "dv": dv}
                            )
                            pbar.update(1) # update pbar for every search config
        self.search_grid = pd.DataFrame(search_grid)
        search_grid = None; gc.collect()
        if verbose:
            print(f"search-grid-shape: {self.search_grid.shape}")
        if inplace:
            return self

    def save(self, 
            filepath: str="search_grid", 
            data: Optional[pd.DataFrame]=None, 
            method: str="parquet"
        ):
        """Save the search-grid as a file on the disk."""
        if data is None:
            data = self.search_grid.copy()
        if method == "parquet":
            ext = "parquet"
            data.to_parquet(f"{filepath}.{ext}")

    def transform(self, func: Callable, column: str="returns", 
                  show_progressbar: bool=True, inplace: bool=False):
        """Transform the search-grid and add a target-column."""
        self.target_column = column
        if show_progressbar:
            tqdm.pandas(desc="Transforming")
            self.search_grid[column] = self.search_grid.progress_apply(
                                            func=lambda row: func(row.tolist()), 
                                            axis=1)
        else:
            self.search_grid[column] = self.search_grid.apply(
                                            func=lambda row: func(row.tolist()), 
                                            axis=1)
        if inplace:
            return self

    def make_figures(self,
            base_filename: str="fig_search_grid", 
            num_smallest: int=50, 
            save_figure: bool=True
        ):
        """Make hiplots with search-grid data."""
        fig1 = U.make_hiplot(
            self.search_grid, 
            num_smallest=None, 
            column=self.target_column, # "returns",
        )
        fig2 = U.make_hiplot(
            self.search_grid, 
            num_smallest=num_smallest, 
            column=self.target_column, # "returns",
        )
        if save_figure:
            try:
                fig1.write_image(f"{base_filename}_all.png")
                fig2.write_image(f"{base_filename}_smallest-{num_smallest}.png")
            except ValueError as e:
                print(e)
            finally:
                gc.collect()


def make_search_grid(num_points: int=10):
    """Create search grid."""
    bounds = prepare_bounds(bounds=Config.PARAM_BOUNDS)
    sg = SearchGrid(bounds = bounds)
    sg.create_param_grid(num_points=num_points, inplace=False)
    sg.create_search_grid(inplace=False)
    sg.transform(
        func=DEFAULT_METRIC_FUNC, 
        column="returns", 
        inplace=False,
    )
    return sg


if __name__ == "__main__":
    # install kaleido for saving figure as png file.
    # source: https://stackoverflow.com/questions/59815797/how-to-save-plotly-express-plot-into-a-html-or-static-image-file
    # pip install -Uqq kaleido
    sg = make_search_grid()
    sg.save(filepath="search_grid", method="parquet")
    sg.make_figures(
        base_filename="fig_search_grid", 
        num_smallest=50, 
        save_figure=True
    )
