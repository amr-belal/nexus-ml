import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from src.api.schemas.prediction import HouseFeatures, PredictionResponse
from src.api.core.exceptions import PredictionError, ModelNotFoundError
from src.common.logger import get_logger

logger = get_logger(__name__)


MODELS_DIR = Path(__file__).parent.parent.parent.parent / "models"

class PredictionService:
    def __init__(self):
        self.rf_regressor = None
        self.rf_classifier = None
        self.kmeans = None
        self.scaler = None
        self.feature_columns = None

    def load_models(self):
        try:
            with open(MODELS_DIR / "rf_regressor.pkl", "rb") as f:
                self.rf_regressor = pickle.load(f)
            with open(MODELS_DIR / "rf_classifier.pkl", "rb") as f:
                self.rf_classifier = pickle.load(f)
            with open(MODELS_DIR / "kmeans.pkl", "rb") as f:
                self.kmeans = pickle.load(f)
            with open(MODELS_DIR / "scaler.pkl", "rb") as f:
                self.scaler = pickle.load(f)
            with open(MODELS_DIR / "feature_columns.pkl", "rb") as f:
                self.feature_columns = pickle.load(f)
            logger.info("All models loaded successfully")
        except FileNotFoundError as e:
            raise ModelNotFoundError()  
        
    def _prepare_features(self, house: HouseFeatures) -> pd.DataFrame:
        df = pd.DataFrame(0, index=[0], columns=self.feature_columns)
        
        df['Gr Liv Area'] = house.gr_liv_area
        df['Total Bsmt SF'] = house.total_bsmt_sf
        df['Garage Area'] = house.garage_area
        df['Overall Qual'] = house.overall_qual
        df['Overall Cond'] = house.overall_cond
        df['Year Built'] = house.year_built
        df['Year Remod/Add'] = house.year_remod
        df['Full Bath'] = house.full_bath
        df['Half Bath'] = house.half_bath
        df['Bsmt Full Bath'] = house.bsmt_full_bath
        df['Bsmt Half Bath'] = house.bsmt_half_bath
        df['Fireplaces'] = house.fireplaces
        df['Pool Area'] = house.pool_area
        df['Wood Deck SF'] = house.wood_deck_sf
        df['Open Porch SF'] = house.open_porch_sf
        df['Yr Sold'] = house.yr_sold
        
        # Engineered features
        df['Total_SF'] = house.gr_liv_area + house.total_bsmt_sf + house.garage_area
        df['Total_Porch_SF'] = house.wood_deck_sf + house.open_porch_sf
        df['Total_Bathrooms'] = (house.full_bath + house.bsmt_full_bath +
                                0.5 * house.half_bath + 0.5 * house.bsmt_half_bath)
        df['House_Age'] = house.yr_sold - house.year_built
        df['Remod_Age'] = house.yr_sold - house.year_remod
        df['Was_Remodeled'] = int(house.year_remod != house.year_built)
        df['Total_Quality'] = house.overall_qual + house.overall_cond
        df['Has_Pool'] = int(house.pool_area > 0)
        df['Has_Garage'] = int(house.garage_area > 0)
        df['Has_Fireplace'] = int(house.fireplaces > 0)
    
        logger.info(f"DF columns sample: {df.columns[:5].tolist()}")
        logger.info(f"Gr Liv Area in df: {'Gr Liv Area' in df.columns}")
        logger.info(f"DF dtypes: {df.dtypes.unique()}")
        
        return df
    
    def predict(self, house: HouseFeatures) -> PredictionResponse:
        try:
            features = self._prepare_features(house)
            
            # Regression
            try:
                log_price = self.rf_regressor.predict(features)[0]
                predicted_price = np.expm1(log_price)
                logger.info(f"Regression OK: {predicted_price}")
            except Exception as e:
                logger.error(f"Regression error: {e}")
                raise
            
            # Classification
            try:
                price_category = self.rf_classifier.predict(features)[0]
                logger.info(f"Classification OK: {price_category}")
            except Exception as e:
                logger.error(f"Classification error: {e}")
                raise
            
            # Clustering
            try:
                cluster_features = features[['Total_SF', 'Total_Quality', 'House_Age',
                                            'Total_Bathrooms', 'Total_Porch_SF',
                                            'Has_Garage', 'Has_Fireplace', 
                                            'Overall Qual', 'Gr Liv Area']]
                cluster = int(self.kmeans.predict(cluster_features)[0])
                logger.info(f"Clustering OK: {cluster}")
            except Exception as e:
                logger.error(f"Clustering error: {e}")
                raise

            return PredictionResponse(
                predicted_price=round(predicted_price, 2),
                price_category=price_category,
                cluster=cluster,
                confidence="High"
            )
        except Exception as e:
            raise PredictionError(str(e))
        

prediction_service = PredictionService()