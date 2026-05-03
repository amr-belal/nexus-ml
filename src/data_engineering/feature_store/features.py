import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
from src.common.logger import get_logger

logger = get_logger(__name__)


ORDINAL_MAP = {'None': 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5}

ORDINAL_COLS = [
    'Exter Qual', 'Exter Cond', 'Bsmt Qual', 'Bsmt Cond',
    'Heating QC', 'Kitchen Qual', 'Garage Qual',
    'Garage Cond', 'Pool QC', 'Fireplace Qu'
]

NOMINAL_COLS = [
    'Neighborhood', 'Sale Type', 'Street',
    'Alley', 'Garage Type', 'Foundation'
]

NUMERICAL_COLS = [
    'Total_SF', 'Total_Bathrooms', 'Total_Quality',
    'House_Age', 'Remod_Age', 'Total_Porch_SF',
    'Lot Area', 'Gr Liv Area'
]


class FeatureCreator(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X['Total_SF'] = X['Gr Liv Area'] + X['Total Bsmt SF'] + X['Garage Area']
        X['Total_Porch_SF'] = (X['Wood Deck SF'] + X['Open Porch SF'] +
                               X['Enclosed Porch'] + X['Screen Porch'])
        X['Total_Bathrooms'] = (X['Full Bath'] + X['Bsmt Full Bath'] +
                                0.5 * X['Half Bath'] + 0.5 * X['Bsmt Half Bath'])
        X['House_Age'] = X['Yr Sold'] - X['Year Built']
        X['Remod_Age'] = X['Yr Sold'] - X['Year Remod/Add']
        X['Was_Remodeled'] = (X['Year Remod/Add'] != X['Year Built']).astype(int)
        X['Total_Quality'] = X['Overall Qual'] + X['Overall Cond']
        X['Has_Pool'] = (X['Pool Area'] > 0).astype(int)
        X['Has_Garage'] = (X['Garage Area'] > 0).astype(int)
        X['Has_Fireplace'] = (X['Fireplaces'] > 0).astype(int)
        logger.info(f"Created features, shape: {X.shape}")
        return X

class FeatureEncoder(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.dummy_columns_ = None
        return self

    def transform(self, X):
        X = X.copy()
        for col in ORDINAL_COLS:
            X[col] = X[col].map(ORDINAL_MAP)
        X = pd.get_dummies(X, columns=NOMINAL_COLS)
        self.dummy_columns_ = X.columns.tolist()
        logger.info(f"Encoded features, shape: {X.shape}")
        return X
    

class FeatureScaler(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.scaler = StandardScaler()

    def fit(self, X, y=None):
        self.scaler.fit(X[NUMERICAL_COLS])
        return self

    def transform(self, X):
        X = X.copy()
        X[NUMERICAL_COLS] = self.scaler.transform(X[NUMERICAL_COLS])
        return X