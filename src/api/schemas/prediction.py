from pydantic import BaseModel ,Field
from typing import Optional

class HouseFeatures(BaseModel):
    gr_liv_area: float = Field(..., gt=0, description="Above grade living area in sqft")
    total_bsmt_sf: float = Field(0, ge=0, description="Total basement area in sqft")
    garage_area: float = Field(0, ge=0, description="Garage area in sqft")
    overall_qual: int = Field(..., ge=1, le=10, description="Overall quality 1-10")
    overall_cond: int = Field(..., ge=1, le=10, description="Overall condition 1-10")
    year_built: int = Field(..., ge=1800, le=2025)
    year_remod: int = Field(..., ge=1800, le=2025)
    full_bath: int = Field(0, ge=0)
    half_bath: int = Field(0, ge=0)
    bsmt_full_bath: int = Field(0, ge=0)
    bsmt_half_bath: int = Field(0, ge=0)
    fireplaces: int = Field(0, ge=0)
    pool_area: float = Field(0, ge=0)
    wood_deck_sf: float = Field(0, ge=0)
    open_porch_sf: float = Field(0, ge=0)
    yr_sold: int = Field(2025, ge=2000, le=2025)



class PredictionResponse(BaseModel):
    predicted_price: float
    price_category: str
    cluster: int
    confidence: str