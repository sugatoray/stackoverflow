from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.pipeline import make_pipeline
import numpy as np
import pandas as pd

tscv = TimeSeriesSplit(n_splits = 5)

pipe = make_pipeline(StandardScaler(), MLPRegressor())

param_grid = {
    'mlpregressor__hidden_layer_sizes': [(16, 16,), (64, 64,), (128, 128,)], 
    'mlpregressor__activation': ['identity', 'logistic', 'tanh', 'relu'],
    'mlpregressor__solver': ['adam', 'sgd'],
}

grid = GridSearchCV(pipe, param_grid = param_grid, cv = tscv)

if __name__ == "__main__":

    X_shape = (1000, 10)
    features = np.random.random(X_shape)
    target = np.random.normal(0, 1.0, X_shape[0])

    grid.fit(features, target) # this may not converge because of the randomized data
