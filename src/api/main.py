from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.api.routes.predictions import router as predictions_router
from src.api.services.prediction_service import prediction_service
from src.common.logger import get_logger

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading models...")
    prediction_service.load_models()
    logger.info("Models loaded!")
    yield
    logger.info("Shutting down...")

app = FastAPI(
    title="NexusML API",
    description="Real Estate Price Prediction API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(predictions_router)

@app.get("/health")
async def health():
    return {"status": "ok"}