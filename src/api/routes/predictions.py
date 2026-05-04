from fastapi import APIRouter
from src.api.schemas.prediction import HouseFeatures, PredictionResponse
from src.api.services.prediction_service import prediction_service

router = APIRouter(prefix="/predictions", tags=["predictions"])

@router.post("/predict", response_model=PredictionResponse)
async def predict_price(house: HouseFeatures) -> PredictionResponse:
    return prediction_service.predict(house)