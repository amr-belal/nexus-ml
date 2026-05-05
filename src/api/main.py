from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.api.routes.predictions import router as predictions_router
from src.api.services.prediction_service import prediction_service
from src.api.routes.models import router as models_router
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predictions_router)
app.include_router(models_router)
@app.get("/health")
async def health():
    return {"status": "ok"}