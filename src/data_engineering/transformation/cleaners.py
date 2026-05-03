import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from src.common.logger import get_logger


logger = get_logger(__name__)


NONE_CATEGORICAL = [
    'Pool QC', 'Misc Feature', 'Alley', 'Fence',
    'Fireplace Qu', 'Garage Type', 'Garage Finish',
    'Garage Qual', 'Garage Cond', 'Bsmt Qual',
    'Bsmt Cond', 'Bsmt Exposure', 'BsmtFin Type 1',
    'BsmtFin Type 2', 'Mas Vnr Type'
]

ZERO_NUMERICAL = [
    'Lot Frontage', 'Garage Yr Blt', 'Mas Vnr Area',
    'BsmtFin SF 1', 'BsmtFin SF 2', 'Bsmt Unf SF',
    'Total Bsmt SF', 'Bsmt Full Bath', 'Bsmt Half Bath',
    'Garage Cars', 'Garage Area'
]


class MissingValueHandler(BaseEstimator , TransformerMixin):
    def fit(self , X , y=None):
        self.electrical_mode = X['Electrical'].mode()[0]
        return self
    
    def transform(self , X):
        X = X.copy()
        X[NONE_CATEGORICAL] = X[NONE_CATEGORICAL].fillna("None")
        X[ZERO_NUMERICAL] = X[ZERO_NUMERICAL].fillna(0)
        X['Electrical'] = X['Electrical'].fillna(self.electrical_mode)
        logger.info(f"Missing values after cleaning: {X.isnull().sum().sum()}")
        return X

