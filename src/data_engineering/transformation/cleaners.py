import pandas as pd 
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

def handle_missing_values(df :pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df[NONE_CATEGORICAL] = df[NONE_CATEGORICAL].fillna("None")
    df[ZERO_NUMERICAL] = df[ZERO_NUMERICAL].fillna(0)
    df['Electrical'] = df['Electrical'].fillna(df['Electrical'].mode()[0])
    logger.info(f"Missing values after cleaning: {df.isnull().sum().sum()}")
    return df


