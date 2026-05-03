from pydantic_settings import BaseSettings
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent

class Settings(BaseSettings):
    RAW_DATA_DIR: Path = ROOT_DIR / "data" / "raw"
    INTERIM_DATA_DIR: Path = ROOT_DIR / "data" / "interim"
    PROCESSED_DATA_DIR: Path = ROOT_DIR / "data" / "processed"
    MLFLOW_TRACKING_URI: str = "sqlite:///mlruns.db"
    EXPERIMENT_NAME: str = "nexusml-real-estate"

    class Config:
        env_file = ".env"

settings = Settings()