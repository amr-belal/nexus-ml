from pathlib import Path
import pandas as pd 
from src.common.logger import get_logger
from src.common.config import settings

logger = get_logger(__name__)

def load_raw_data(filename:str) -> pd.DataFrame:
    path = settings.RAW_DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"file not found {path}")
    logger.info(f"loading data from {path}")
    df = pd.read_csv(path)
    logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    return df