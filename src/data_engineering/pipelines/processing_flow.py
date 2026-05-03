from sklearn.pipeline import Pipeline
from src.data_engineering.transformation.cleaners import MissingValueHandler
from src.data_engineering.feature_store.features import (
    FeatureCreator,FeatureEncoder,FeatureScaler
)

from src.common.logger import get_logger


logger = get_logger(__name__)


def build_pipeline()-> Pipeline:
    return Pipeline([
        ('missing_values', MissingValueHandler()),
        ('feature_creator', FeatureCreator()),
        ('feature_encoder', FeatureEncoder()),
        ('feature_scaler', FeatureScaler()),
    ])


#=====output=============
#Final shape: (2930, 142)
# Pipeline works!